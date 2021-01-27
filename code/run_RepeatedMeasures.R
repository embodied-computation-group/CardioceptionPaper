#####################################

# Estimate metacognitive efficiency (Mratio) at the group level
#
# Adaptation in R of matlab function 'fit_meta_d_mcmc_groupCorr.m'
# by Steve Fleming 
# for more details see Fleming (2017). HMeta-d: hierarchical Bayesian 
# estimation of metacognitive efficiency from confidence ratings. 
#
# you need to install the following packing before using the function:
# tidyverse
# magrittr
# reshape2
# rjags
# coda
# lattice
# broom
# ggpubr
# ggmcmc
#
# nR_S1 and nR_S2 should be two lists of each nR_S1 or nR_S2 per task
# model output is a large mcmc list and two vectors for d1 and c1
#
# Author: Nicolas Legrand (nicolas.legrand@cfin.au.dk)

#####################################

## Packages
library(tidyverse)
library(magrittr)
library(reshape2)
library(rjags)
library(coda)
library(lattice)
library(broom)
library(ggpubr)
library(ggmcmc)


input = read.csv(file.path(dirname(getwd()), 'data/responsesRatings.txt'))

input = filter(input, Session=="Del2")
subjects = unique(input$Subject)

nR_S1_tot = list()
nR_S2_tot = list()
for (sub in subjects){
  nR_S1_cond = list()
  nR_S2_cond = list()
  for (cond in c('Intero', 'Extero')){
    nR_S1_cond[[length(nR_S1_cond) + 1]] <- filter(input, Subject==sub, Modality==cond)$nR_S1
    nR_S2_cond[[length(nR_S2_cond) + 1]] <- filter(input, Subject==sub, Modality==cond)$nR_S2
  }
  nR_S1_tot[[length(nR_S1_tot) + 1]] <- nR_S1_cond
  nR_S2_tot[[length(nR_S2_tot) + 1]] <- nR_S2_cond
}

# Model -------------------------------------------------------------------

# Fit all data at once
source("Function_metad_1wayANOVA.R")
output <- metad_1wayANOVA(nR_S1 = nR_S1_tot, nR_S2 = nR_S2_tot)

## Summary stats --------------------------------------------------

# Mean values 
Value <- summary(output)
stat <- data.frame(mean = Value[["statistics"]][, "Mean"])
stat %<>%
  rownames_to_column(var = "name")

# Rhat 
Value <- gelman.diag(output, confidence = 0.95)
Rhat <- data.frame(conv = Value$psrf)

# HDI 
HDI <- data.frame(HPDinterval(output, prob = 0.95))
HDI %<>%
  rownames_to_column(var = "name")

# All values in the same dataframe
Fit <- stat %>%
  cbind(lower = HDI$lower,
        upper = HDI$upper)

## Plots ---------------------------------------------------------

# Plot trace mcmc
traceplot(output)

# mcmc values in df for plot posterior distributions
mcmc.sample <- ggs(output)

# Plot posterior distribution for rho value
PlotCondition1 <- mcmc.sample %>%
  filter(Parameter == "muBd_Condition1") %>% 
  ggplot(aes(value)) +
  geom_histogram(fill = "blue", colour = "grey", alpha = 0.5, bins = 100) +
  geom_vline(xintercept = stat$mean[stat$name == "muBd_Condition1"],linetype="dashed", size = 1.) +
  geom_vline(xintercept = 0, size = 1.5, color='red') +
  geom_segment(aes(x = HDI$lower[HDI$name == "muBd_Condition1"], y = 50, xend = HDI$upper[HDI$name == "muBd_Condition1"], yend = 50), colour = "white", size = 2.5) +
  ylab("Sample count") +
  xlab(expression(paste("muBd_Condition1")))
PlotCondition1

# Save samples ------------------------------------------------------------

df = rbind(data.frame(output[[1]]), data.frame(output[[2]]), data.frame(output[[3]]))



write.table(stat, file = file.path(dirname(getwd()), 'data/jagsStats_Del1.txt'), append = FALSE, sep = "\t", dec = ".",
            row.names = TRUE, col.names = TRUE)

jagsSamples <- mcmc.sample %>%
  filter(Parameter == "muBd_Condition1")

write.table(jagsSamples, file = file.path(dirname(getwd()), 'data/jagsSamples_Del1.txt'), append = FALSE, sep = "\t", dec = ".",
            row.names = TRUE, col.names = TRUE)
