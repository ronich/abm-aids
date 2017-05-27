#
# analyze NetLogo BehaviorSpace output
#
rm(list = ls())

# 0. Packages initialization, folder for plots----

# install.packages("plyr")
# install.packages("lattice")
# install.packages("mgcv")
# install.packages("DiceKriging")
# install.packages("rgl")
# install.packages("scatterplot3d")
library(plyr)
library(lattice)
library(mgcv)
library(DiceKriging)
library(rgl)
library(scatterplot3d)

if(dir.exists('plots') == FALSE){
  dir.create('plots')
}
# 1. read the Behav
# iorSpace experiment output----
results <- read.csv("aids_output.txt", sep=";", header=FALSE, dec='.')
head(results)
names(results)
names(results) <- c("iter1", "iter2", "ccept_use", "test_freq", "ss_time", "pcnt_infected") #ss_time od steady state time :)

results$ccept_use <- results$ccept_use * 100
results$test_freq <- results$test_freq * 100
results$pcnt_infected <- results$pcnt_infected * 100


zlim <- range(results$pcnt_infected)
zlen <- zlim[2] - zlim[1] + 1
zlen

# 2. aggregate results----

sum.data = ddply(results, .(ccept_use, test_freq), summarize,
                 m_pcnt_infected = mean(pcnt_infected),
                 sd_pcnt_infected = sd(pcnt_infected))
sum.data <- sum.data[order(sum.data$ccept_use, sum.data$test_freq),]
# head(sum.data)

# 2.1 Average infected percentage----

summary(sum.data)

# 3. visualize metamodel response surface----
# c_ - counterplot
# w_ - wideframe

png('plots/c_basic_model.png')
contourplot(m_pcnt_infected ~ ccept_use + test_freq, data = sum.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen),
            xlab = "Szansa na u¿ycie antykoncepcji (%)",
            ylab = "Szansa na zbadanie siê (%)", pch = 19)
dev.off()
# png('plots/w_basic_model.png')
# wireframe(m_pcnt_infected ~ ccept_use + test_freq, data = sum.data,
#           drape = TRUE, colorkey = TRUE, pretty = T, region = T,
#           cuts = 10, region = T, col.regions = terrain.colors(zlim),
#           xlab = "U¿ycie antykoncepcji", ylab = "Badania",
#           zlab = "Zara¿eni")
png('plots/w_basic_model.png')
with(sum.data, {
  scatterplot3d(ccept_use,   # x axis
                test_freq,     # y axis
                m_pcnt_infected,    # z axis
                type = "p", highlight.3d = T, pch = 16, angle = 315,
                col.grid="lightblue", col.axis="blue",
                xlab = "U¿ycie antykoncepcji", ylab = "Badania",
                zlab = "Zara¿eni", main = "Odsetek zara¿onych w zale¿noœci od 
                czêstotliwoœci badañ i u¿ycia antykoncepcji")
})
dev.off()

# 4. generate a new set of points for metamodel prediction----
range.for.ccept_use <- range(results$ccept_use)      # range for ccept_use
range.for.test_freq <- range(results$test_freq)  # range for test_freq
ccept_use_range <-   seq(range.for.ccept_use[1], range.for.ccept_use[2])
test_freq_range <- seq(range.for.test_freq[1], range.for.test_freq[2])
new.data <- expand.grid(ccept_use_range, test_freq_range)
colnames(new.data) <- c("ccept_use", "test_freq")
head(new.data)

# 5. our 1st metamodel----
m1 <- lm(pcnt_infected ~ ccept_use + test_freq, data = results)
summary(m1)
# visualize metamodel response surface
new.data$pcnt_infected.hat <- predict(m1, newdata = new.data)
png('plots/c_1st_meta.png')
contourplot(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen),
            xlab  = "Szansa na u¿ycie antykoncepcji (%)",
            ylab = "Szansa na zbadanie siê (%)", main = "Model liniowy")
dev.off()
png('plots/w_1st_meta.png')
wireframe(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
          drape = TRUE, colorkey = F, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlen),
          xlab = "U¿ycie antykoncepcji", ylab = "Badania",
          zlab = "Zara¿eni", shade = T, screen = list(z = 220, x = -60),
          scales = list(arrows = F, col = "black"), par.settings = par.set,
          main = "Model liniowy")
dev.off()

# 6. make a better linear model with parameter interaction----
m2 <- lm(pcnt_infected ~ ccept_use * test_freq, data = results)
summary(m2)
# visualize metamodel response surface
new.data$pcnt_infected.hat <- predict(m2, newdata = new.data)
png('plots/c_interaction.png')
contourplot(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen),
            main = "Model z interakcj¹", xlab = "Szansa na u¿ycie antykoncepcji (%)",
            ylab = "Szansa na zbadanie siê (%)")
dev.off()
png('plots/w_interaction.png')
wireframe(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
          drape = TRUE, colorkey = F, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlen),
          xlab = "U¿ycie antykoncepcji", ylab = "Badania",
          zlab = "Zara¿eni", shade = T, screen = list(z = 220, x = -60),
          scales = list(arrows = F), par.settings = par.set,
          main = "Model z interakcj¹")
dev.off()

# 7. nonlinearity - logarithms-----
m3 <- lm(pcnt_infected ~ (ccept_use + test_freq + log(ccept_use) + log(test_freq))^2, data = results)
summary(m3)
# visualize metamodel response surface
new.data$pcnt_infected.hat <- predict(m3, newdata = new.data)
png('plots/c_log.png')
contourplot(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen),
            xlab = "Szansa na u¿ycie antykoncepcji (%)",
            ylab = "Szansa na zbadanie siê (%)",
            main = "Model z logarytmami i interakcjami")
dev.off()
png('plots/w_log.png')
# wireframe(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
#           drape = TRUE, colorkey = F, pretty = T, region = T,
#           cuts = 10, region = T, col.regions = terrain.colors(zlim),
#           xlab = "U¿ycie antykoncepcji", ylab = "Badania",
#           zlab = "Zara¿eni", shade = T, screen = list(z = 140, x = -60),
#           scales = list(arrows = F))
wireframe(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
          drape = TRUE, colorkey = F, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlim),
          xlab = "U¿ycie antykoncepcji", ylab = "Badania",
          zlab = "Zara¿eni", shade = T, screen = list(z = 220, x = -60),
          scales = list(arrows = F), par.settings = par.set,
          main = "Model z logarytmami i interakcjami")
dev.off()

# 8. nonlinearity - squares----

m4 <- lm(pcnt_infected ~ (ccept_use + test_freq + I(ccept_use^2) + I(test_freq^2))^2, data = results)
summary(m4)
# visualize metamodel response surface
new.data$pcnt_infected.hat <- predict(m4, newdata = new.data)
png('plots/c_squares.png')
contourplot(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen),
            xlab = "Szansa na u¿ycie antykoncepcji (%)",
            ylab = "Szansa na zbadanie siê (%)",
            main = "Model z kwadratami zmiennych i interakcjami")
dev.off()
png('plots/w_squares.png')
wireframe(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
          drape = TRUE, colorkey = F, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlim),
          xlab = "U¿ycie antykoncepcji", ylab = "Badania",
          zlab = "Zara¿eni", shade = T, screen = list(z = 220, x = -60),
          scales = list(arrows = F), par.settings = par.set,
          main = "Model z kwadratami zmiennych i interakcjami")
dev.off()


# 9. GAM----

m5 <- gam(pcnt_infected ~ s(ccept_use) + s(test_freq), data = results)
summary(m5)
# visualize metamodel response surface
new.data$pcnt_infected.hat <- predict(m5, newdata = new.data)
png('plots/c_gam.png')
contourplot(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen),
            xlab = "Szansa na u¿ycie antykoncepcji (%)",
            ylab = "Szansa na zbadanie siê (%)",
            main = "GAM")
dev.off()
png('plots/w_gam.png')
wireframe(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
          drape = TRUE, colorkey = F, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlim),
          xlab = "U¿ycie antykoncepcji", ylab = "Badania",
          zlab = "Zara¿eni", shade = T, screen = list(z = 220, x = -60),
          scales = list(arrows = F), par.settings = par.set, main = 'GAM')
dev.off()
# wireframe(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
#           drape = TRUE, colorkey = F, pretty = T, region = T,
#           cuts = 10, region = T, col.regions = terrain.colors(zlim),
#           xlab = "U¿ycie antykoncepcji", ylab = "Badania",
#           zlab = "Zara¿eni", shade = T)
dev.off()
plot(m4)


#

# 10. stochastic kriging metamodel----

# stoch. kriging
m6 <- km(m_pcnt_infected ~ ., 
         sum.data[,1:2], sum.data[,3],
         covtype = "gauss",
         noise.var = sum.data[,4])
# visualize metamodel response surface
new.data$pcnt_infected.hat <- predict(m6, newdata = new.data[,1:2], type='SK')$mean
png('plots/c_stoch_kring.png')
contourplot(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen),
            xlab = "Szansa na u¿ycie antykoncepcji (%)",
            ylab = "Szansa na zbadanie siê (%)",
            main = "Stochastic kringing")
dev.off()
png('plots/w_stoch_kring.png')
wireframe(pcnt_infected.hat ~ ccept_use + test_freq, data = new.data,
          drape = TRUE, colorkey = F, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlim),
          xlab = "U¿ycie antykoncepcji", ylab = "Badania",
          zlab = "Zara¿eni", shade = T, screen = list(z = 220, x = -60),
          scales = list(arrows = F), par.settings = par.set,
          main = 'Stochastic kringing')
dev.off()

with(new.data, plot3d(ccept_use,   # x axis
                      test_freq,     # y axis
                      pcnt_infected.hat, col = heat.colors(1000)))

# 11. 3D visualization with rgl----
#
library(rgl)
with(new.data, {
  pcnt_infected.hat.m <- matrix(pcnt_infected.hat, length(ccept_use_range))
  colorlut <- terrain.colors(zlen) # height color lookup table
  col <- colorlut[pcnt_infected.hat.m - zlim[1] + 1 ] # assign colors to heights for each point
  persp3d(ccept_use_range,test_freq_range, pcnt_infected.hat.m, color = col)
  grid3d(c("x", "y", "z"))
})

# 12. play animation----
play3d(spin3d(axis = c(0, 0, 1), rpm = 4), duration = 15)
