#
# analyze NetLogo BehaviorSpace output
#

# read the BehaviorSpace experiment output
results <- read.csv("Schelling.csv")
head(results)
names(results)
names(results) <- c("run.number", "dens", "sw", "step", "ps")

zlim <- range(results$ps)
zlen <- zlim[2] - zlim[1] + 1
zlen

# aggregate results
library(plyr)
sum.data = ddply(results, .(sw, dens), summarize,
                 m_ps = mean(ps),
                 sd_ps = sd(ps))
sum.data <- sum.data[order(sum.data$dens, sum.data$sw),]
head(sum.data)

# visualize metamodel response surface
library(lattice)
contourplot(m_ps ~ sw + dens, data = sum.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen))
wireframe(m_ps ~ sw + dens, data = sum.data,
          drape = TRUE, colorkey = TRUE, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlim))


# generate a new set of points for metamodel prediction
sw_range <- range(results$sw)      # range for similar.wanted
dens_range <- range(results$dens)  # range for densisty
swrange <-   seq(sw_range[1], sw_range[2])
densrange <- seq(dens_range[1], dens_range[2])
new.data <- expand.grid(swrange, densrange)
colnames(new.data) <- c("sw", "dens")
head(new.data)

# our 1st metamodel
m1 <- lm(ps ~ sw + dens, data = results)
summary(m1)
# visualize metamodel response surface
new.data$pshat <- predict(m1, newdata = new.data)
contourplot(pshat ~ sw + dens, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen))
wireframe(pshat ~ sw + dens, data = new.data,
          drape = TRUE, colorkey = TRUE, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlen))

# make a better linear model with parameter interaction
m2 <- lm(ps ~ sw * dens, data = results)
summary(m2)
# visualize metamodel response surface
new.data$pshat <- predict(m2, newdata = new.data)
contourplot(pshat ~ sw + dens, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen))
wireframe(pshat ~ sw + dens, data = new.data,
          drape = TRUE, colorkey = TRUE, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlen))

# try to make it even better by adding nonlinearity
m3 <- lm(ps ~ (sw + dens + log(sw) + log(dens))^2, data = results)
summary(m3)
# visualize metamodel response surface
new.data$pshat <- predict(m3, newdata = new.data)
contourplot(pshat ~ sw + dens, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen))
wireframe(pshat ~ sw + dens, data = new.data,
          drape = TRUE, colorkey = TRUE, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlim))


# GAM
library(mgcv)

m4 <- gam(ps ~ s(sw) + s(dens), data = results)
summary(m4)
# visualize metamodel response surface
new.data$pshat <- predict(m4, newdata = new.data)
contourplot(pshat ~ sw + dens, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen))
wireframe(pshat ~ sw + dens, data = new.data,
          drape = TRUE, colorkey = TRUE, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlim))
plot(m3)


#
# stochastic kriging metamodel
#

library(DiceKriging)
?km()
# stoch. kriging
m5 <- km(m_ps ~ ., 
         sum.data[,1:2], sum.data[,3],
         covtype = "gauss",
         noise.var = sum.data[,4])
# visualize metamodel response surface
new.data$pshat <- predict(m5, newdata = new.data[,1:2], type='SK')$mean
contourplot(pshat ~ sw + dens, data = new.data,
            cuts = 20, region = T, col.regions = terrain.colors(zlen))
wireframe(pshat ~ sw + dens, data = new.data,
          drape = TRUE, colorkey = TRUE, pretty = T, region = T,
          cuts = 10, region = T, col.regions = terrain.colors(zlim))


#
# 3D visualization with rgl
#

library(rgl)
with(new.data, {
  psm <- matrix(pshat, length(swrange))
  colorlut <- terrain.colors(zlen) # height color lookup table
  col <- colorlut[ psm - zlim[1] + 1 ] # assign colors to heights for each point
  persp3d(swrange,densrange, psm, color = col)
  grid3d(c("x", "y", "z"))
})

# play animation
play3d(spin3d(axis = c(0, 0, 1), rpm = 4), duration = 15)
