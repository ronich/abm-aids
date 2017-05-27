#
# analyze NetLogo BehaviorSpace output
#

rm(list = ls())

# read the BehaviorSpace experiment output
results <- read.csv("aids_output_3.txt", sep=";", header=FALSE, dec='.')
head(results)
names(results)
names(results) <- c("iter1", "iter2", "ccept_use", "test_freq", "ss_time", "pcnt_infected") #ss_time od steady state time :)

results$ccept_use <- results$ccept_use * 100
results$test_freq <- results$test_freq * 100
results$pcnt_infected <- results$pcnt_infected * 100


zlim <- range(results$pcnt_infected)
zlen <- zlim[2] - zlim[1] + 1
zlen


# aggregate results
#install.packages("plyr")
library(plyr)
sum.data = ddply(results, .(ccept_use, test_freq), summarize,
                 m_pcnt_infected = mean(pcnt_infected),
                 sd_pcnt_infected = sd(pcnt_infected))
sum.data <- sum.data[order(sum.data$ccept_use, sum.data$test_freq),]
head(sum.data)

# visualize metamodel response surface
library(lattice)
contourplot(m_pcnt_infected ~ ccept_use + test_freq, data = sum.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen))
wireframe(m_pcnt_infected ~ ccept_use + test_freq, data = sum.data,
          drape = TRUE, colorkey = TRUE, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlim))


# generate a new set of points for metamodel prediction
range.for.ccept_use <- range(results$ccept_use)      # range for ccept_use
range.for.test_freq <- range(results$test_freq)  # range for test_freq
ccept_use_range <-   seq(range.for.ccept_use[1], range.for.ccept_use[2])
test_freq_range <- seq(range.for.test_freq[1], range.for.test_freq[2])
new.data <- expand.grid(ccept_use_range, test_freq_range)
colnames(new.data) <- c("ccept_use", "test_freq")
head(new.data)

# our 1st metamodel
m1 <- lm(pcnt_infected ~ ccept_use + test_freq, data = results)
summary(m1)
# visualize metamodel response surface
new.data$pcnt_infected.hat <- predict(m1, newdata = new.data)
contourplot(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen))
wireframe(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
          drape = TRUE, colorkey = TRUE, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlen))

# make a better linear model with parameter interaction
m2 <- lm(pcnt_infected ~ ccept_use * test_freq, data = results)
summary(m2)
# visualize metamodel response surface
new.data$pcnt_infected.hat <- predict(m2, newdata = new.data)
contourplot(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen))
wireframe(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
          drape = TRUE, colorkey = TRUE, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlen))

# try to make it even better by adding nonlinearity
m3 <- lm(pcnt_infected ~ (ccept_use + test_freq + log(ccept_use) + log(test_freq))^2, data = results)
summary(m3)
# visualize metamodel response surface
new.data$pcnt_infected.hat <- predict(m3, newdata = new.data)
contourplot(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen))
wireframe(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
          drape = TRUE, colorkey = TRUE, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlim))


# GAM
library(mgcv)

m4 <- gam(pcnt_infected ~ s(ccept_use) + s(test_freq), data = results)
summary(m4)
# visualize metamodel response surface
new.data$pcnt_infected.hat <- predict(m4, newdata = new.data)
contourplot(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen))
wireframe(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
          drape = TRUE, colorkey = TRUE, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlim))
plot(m3)


#
# stochastic kriging metamodel
#

#install.packages("DiceKriging")
library(DiceKriging)
?km()
# stoch. kriging
m5 <- km(m_pcnt_infected ~ ., 
         sum.data[,1:2], sum.data[,3],
         covtype = "gauss",
         noise.var = sum.data[,4])
# visualize metamodel response surface
new.data$pcnt_infected.hat <- predict(m5, newdata = new.data[,1:2], type='SK')$mean
contourplot(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen))
wireframe(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
          drape = TRUE, colorkey = TRUE, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlim))


#
# 3D visualization with rgl
#

library(rgl)
with(new.data, {
  pcnt_infected.hat.m <- matrix(pcnt_infected.hat, length(ccept_use_range))
  colorlut <- terrain.colors(zlen) # height color lookup table
  col <- colorlut[pcnt_infected.hat.m - zlim[1] + 1 ] # assign colors to heights for each point
  persp3d(ccept_use_range,test_freq_range, pcnt_infected.hat.m, color = col)
  grid3d(c("x", "y", "z"))
})

# play animation
play3d(spin3d(axis = c(0, 0, 1), rpm = 4), duration = 15)
