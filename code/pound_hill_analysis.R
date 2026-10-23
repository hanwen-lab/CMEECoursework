pound_hill <- read.csv(
  "data/pound_hill_data.csv",
  header = FALSE,
  check.names = FALSE,
  na.strings = ""
)

metadata <- read.csv(
  "data/pound_hill_meta_data.csv",
  header = TRUE,
  sep = ";",
  stringsAsFactors = FALSE
)

species_names <- pound_hill[5:nrow(pound_hill), 1]

sampling_info <- as.data.frame(t(pound_hill[1:4, -1]))
colnames(sampling_info) <- c(
  "Cultivation",
  "Block",
  "Plot",
  "Quadrat"
)

species_counts <- pound_hill[-(1:4), -1]
colnames(species_counts) <- species_names
rownames(species_counts) <- NULL

species_counts[] <- lapply(species_counts, as.numeric)
species_counts[is.na(species_counts)] <- 0

stopifnot(all(sapply(species_counts, is.numeric)))
stopifnot(all(as.matrix(species_counts) >= 0))

n_species <- nrow(species_counts)
n_quadrats <- ncol(species_counts)
n_plots <- length(unique(sampling_info$Plot))

print(n_species)
print(n_quadrats)
print(n_plots)

sampling_info$Richness <- colSums(species_counts > 0)
sampling_info$Abundance <- colSums(species_counts)

plot_summary <- aggregate(
  cbind(Richness, Abundance) ~ Cultivation + Block + Plot,
  data = sampling_info,
  FUN = mean
)

colnames(plot_summary)[4:5] <- c(
  "MeanRichness",
  "MeanAbundance"
)

print(plot_summary)
print(table(plot_summary$Cultivation))

write.csv(
  plot_summary,
  "results/pound_hill_plot_richness.csv",
  row.names = FALSE
)

pdf("results/pound_hill_plot_richness.pdf")

boxplot(
  MeanRichness ~ Cultivation,
  data = plot_summary,
  xlab = "Cultivation treatment",
  ylab = "Mean species richness per plot",
  main = "Pound Hill: plot-level species richness",
  col = "lightblue"
)

stripchart(
  MeanRichness ~ Cultivation,
  data = plot_summary,
  vertical = TRUE,
  method = "jitter",
  add = TRUE,
  pch = 19,
  col = "darkred"
)

boxplot(
  MeanAbundance ~ Cultivation,
  data = plot_summary,
  xlab = "Cultivation treatment",
  ylab = "Mean total abundance per quadrat",
  main = "Pound Hill: plot-level total abundance",
  col = "lightblue"
)

stripchart(
  MeanAbundance ~ Cultivation,
  data = plot_summary,
  vertical = TRUE,
  method = "jitter",
  add = TRUE,
  pch = 19,
  col = "darkred"
)

dev.off()


