library(ggplot2)
library(dplyr)
library(reshape2)
library(gridExtra)

data <- read.csv('./data/data.csv')
data$description = as.factor(data$description)
data$radius = as.numeric(data$radius)
data$criticality = as.numeric(data$criticality)
data$criticality.std = as.numeric(data$criticality.std)

data$thermal.fission = as.numeric(data$thermal.fission)
data$epithermal.fission = as.numeric(data$epithermal.fission)
data$fast.fission = as.numeric(data$fast.fission)

criticality.plot = ggplot(data, aes(x = radius, y = criticality, colour = description)) +
    geom_errorbar(aes(ymin = criticality - criticality.std, ymax = criticality + criticality.std), width=0.1) +
    geom_line() +
    geom_point() + 
    xlab('Moderator Thickness (cm)') +
    ylab('Criticality Value') +
    ggtitle('Criticality of a Moderated Sphere of Uranium')
ggsave(criticality.plot, file="./plots/criticality-plot.eps", width=9, height=6)

distilled.data = select(data, radius, description, fast.fission, epithermal.fission, thermal.fission)

flibe.natural <- melt(select(filter(distilled.data, description == 'FLiBe w/ Natural Li'), -description), id.vars = c('radius'))
plot1 <- ggplot(flibe.natural, aes(x = radius, fill = variable, weight = value)) + 
  geom_density(position = 'fill') +
  scale_fill_discrete(name='Neutron Energy',
                      breaks = c('fast.fission', 'epithermal.fission', 'thermal.fission'),
                      labels = c('>100 keV', '0.625 eV - 100 keV', '<0.625 eV')) +
  xlab('Moderator Thickness (cm)') +
  ylab('Neutron Fraction (-)') +
  ggtitle('Energy Spectrum of Neutrons Causing Fission\n\nFLiBe with Natural Lithium')
  ggsave(plot1, file="./plots/flibe-natural.eps", width=9, height=6)

flibe.enriched <- melt(select(filter(distilled.data, description == 'FLiBe w/ Enriched Li'), -description), id.var=c('radius'))
plot2 <- ggplot(flibe.enriched, aes(x = radius, fill = variable, weight = value)) + 
  geom_density(position = 'fill') +
  scale_fill_discrete(name='Neutron Energy',
                      breaks = c('fast.fission', 'epithermal.fission', 'thermal.fission'),
                      labels = c('>100 keV', '0.625 eV - 100 keV', '<0.625 eV')) +
  xlab('Moderator Thickness (cm)') +
  ylab('Neutron Fraction (-)') +
  ggtitle('Energy Spectrum of Neutrons Causing Fission\n\nFLiBe with Enriched Lithium')
  ggsave(plot2, file="./plots/flibe-enriched.eps", width=9, height=6)

graphite <- melt(select(filter(distilled.data, description == 'Graphite'), -description), id.var=c('radius'))
plot3 <- ggplot(graphite, aes(x = radius, fill = variable, weight = value)) + 
  geom_density(position = 'fill') +
  scale_fill_discrete(name='Neutron Energy',
                      breaks = c('fast.fission', 'epithermal.fission', 'thermal.fission'),
                      labels = c('>100 keV', '0.625 eV - 100 keV', '<0.625 eV')) +
  xlab('Moderator Thickness (cm)') +
  ylab('Neutron Fraction (-)') +
  ggtitle('Energy Spectrum of Neutrons Causing Fission\n\nGraphite')
  ggsave(plot3, file="./plots/graphite.eps", width=9, height=6)

setEPS()
postscript("./plots/composite.eps", width = 11, height = 6)
composite <- grid.arrange(criticality.plot, plot1, plot2, plot3, ncol=2)
dev.off()