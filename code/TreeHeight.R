TreeHeight <- function(degrees, distance) {
    radians <- degrees * pi / 180
    height <- distance * tan(radians)
    return(height)
}

trees <- read.csv("data/trees.csv", header = TRUE)
names(trees)
head(trees)
required_columns <- c(
  "Species",
  "Distance.m",
  "Angle.degrees"
)

if (!all(required_columns %in% names(trees))) {
  stop("Input error: one or more required columns are missing.")
}

valid_distance <- trees$Distance.m > 0 &
                  trees$Distance.m <= 100

if (!all(valid_distance)) {
  stop("Invalid Distance.m values!")
}

valid_angle <- trees$Angle.degrees > 0 &
               trees$Angle.degrees < 90

if (!all(valid_angle)) {
  stop("Invalid Angle.degrees values!")
}

trees$height_m <- TreeHeight(
  trees$Angle.degrees,
  trees$Distance.m
)

dir.create("results", showWarnings = FALSE)

write.csv(
  trees,
  "results/TreeHts.csv",
  row.names = FALSE
)

