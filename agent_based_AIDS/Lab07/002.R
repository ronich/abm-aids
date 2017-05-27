#
# exploring experiment designs
#
n <- 10           # number of design points, consider increasing for more accurate results
dimension <- 2    # dimensionality of the design space

#
# simple random
#
d <- cbind(runif(n), runif(n))
plot(d,xlim=c(0,1),ylim=c(0,1), lab=c(n,n,2), pch=20)
grid(col="black")

# LHS centered
library(DiceDesign)
d <- lhsDesign(n, dimension, randomized = F)
plot(d$design,xlim=c(0,1),ylim=c(0,1), lab=c(n,n,2), pch=20)
grid(col="black")

# LHS randomized
d <- lhsDesign(n,dimension, randomized = T)
plot(d$design,xlim=c(0,1),ylim=c(0,1), lab=c(n,n,2), pch=20)
grid(col="black")

# LHS advanced
library(lhs)
d <- maximinLHS(n, dimension)
plot(d, xlim=c(0,1), ylim=c(0,1), lab=c(n,n,2), pch=20)
grid(col="black")

#
# uniform designs
#
library(randtoolbox)
d <- sobol(n, dimension)
plot(d, xlim=c(0,1), ylim=c(0,1), lab=c(n,n,2), pch=20)
grid(col="black")

d <- halton(n, dimension)
plot(d, xlim=c(0,1), ylim=c(0,1), lab=c(n,n,2), pch=20)
grid(col="black")

#
# design rescaling 
# for fitting the experiment region
#
library(scales)
sw_range <- c(30,75)    # range for similar.wanted
dens_range <- c(50,90)  # range for densisty
exper.design <- cbind(rescale(d[,1], sw_range, c(0,1)),
                  rescale(d[,2], dens_range, c(0,1)))
plot(exper.design, pch=20)
grid(col="black")

