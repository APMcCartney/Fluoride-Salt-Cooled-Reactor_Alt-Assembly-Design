library(ggplot2)
library(dplyr)
library(reshape2)
library(gridExtra)

data <- read.csv('./data/data.csv')
data$description = as.factor(data$description)
data$margin = as.numeric(data$margin)
data$criticality = as.numeric(data$criticality)
data$criticality.std = as.numeric(data$criticality.std)

data$thermal.fission = as.numeric(data$thermal.fission)
data$epithermal.fission = as.numeric(data$epithermal.fission)
data$fast.fission = as.numeric(data$fast.fission)

criticality.plot = ggplot(data, aes(x = margin, y = criticality, colour = description)) +
    geom_errorbar(aes(ymin = criticality - criticality.std, ymax = criticality + criticality.std), width=0.1) +
    geom_line() +
    geom_point() + 
    xlab('Moderator Thickness (cm)') +
    ylab('Criticality Value') +
    ggtitle('Criticality of a Lattice of\nModerated Uranium Spheres')
ggsave(criticality.plot, file="./plots/criticality-plot.eps", width=9, height=6)

plot0 <- ggplot(data, aes(x = margin, y = energy.fission.causing.neutrons, colour = description)) +
  geom_line() +
  geom_point() +
  xlab('Moderator Thickness (cm)') +  
  ylab('Energy (MeV)') +
  ggtitle('Mean Energy of Neutrons causing Fission\nin a Lattice of Moderated Uranium Spheres')
ggsave( plot0, file="./plots/energy-plot.eps", width=9, height=6)

distilled.data = select(data, margin, description, fast.fission, epithermal.fission, thermal.fission)

flibe.natural <- melt(select(filter(distilled.data, description == 'FLiBe w/ Natural Li'), -description), id.vars = c('margin'))
plot1 <- ggplot(flibe.natural, aes(x = margin, fill = variable, weight = value)) + 
  geom_density(position = 'fill') +
  scale_fill_discrete(name='Neutron Energy',
                      breaks = c('fast.fission', 'epithermal.fission', 'thermal.fission'),
                      labels = c('>100 keV', '0.625 eV - 100 keV', '<0.625 eV')) +
  xlab('Moderator Thickness (cm)') +
  ylab('Neutron Fraction (-)') +
  ggtitle('Energy Spectrum of Neutrons Causing Fission\n\nFLiBe with Natural Lithium')
  ggsave(plot1, file="./plots/flibe-natural.eps", width=9, height=6)

flibe.enriched <- melt(select(filter(distilled.data, description == 'FLiBe w/ Enriched Li'), -description), id.var=c('margin'))
plot2 <- ggplot(flibe.enriched, aes(x = margin, fill = variable, weight = value)) + 
  geom_density(position = 'fill') +
  scale_fill_discrete(name='Neutron Energy',
                      breaks = c('fast.fission', 'epithermal.fission', 'thermal.fission'),
                      labels = c('>100 keV', '0.625 eV - 100 keV', '<0.625 eV')) +
  xlab('Moderator Thickness (cm)') +
  ylab('Neutron Fraction (-)') +
  ggtitle('Energy Spectrum of Neutrons Causing Fission\n\nFLiBe with Enriched Lithium')
  ggsave(plot2, file="./plots/flibe-enriched.eps", width=9, height=6)

graphite <- melt(select(filter(distilled.data, description == 'Graphite'), -description), id.var=c('margin'))
plot3 <- ggplot(graphite, aes(x = margin, fill = variable, weight = value)) + 
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
composite <- grid.arrange(plot0, plot1, plot2, plot3, ncol=2)
dev.off()