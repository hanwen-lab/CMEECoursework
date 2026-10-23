args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
stop("Error: Please provide a CSV file path, e.g. data/trees.csv")
}

if (length(args) != 1) {
stop("Error: Please provide exactly one CSV file path.")
}

input_file <- args[1]

trees <- read.csv(input_file, header = TRUE)

required_columns <- c(
  "Species",
  "Distance.m",
  "Angle.degrees"
)

if (!identical(names(trees), required_columns)) {
  stop("Error: The CSV must contain the columns Species, Distance.m, and Angle.degrees in this order.")
}

if (!is.numeric(trees$Distance.m) ||
    !is.numeric(trees$Angle.degrees)) {
  stop("Error: Distance.m and Angle.degrees must be numeric.")
}

if (any(!is.finite(trees$Distance.m)) ||
    any(!is.finite(trees$Angle.degrees))) {
  stop("Error: Distance.m and Angle.degrees must contain finite values.")
}

valid_distance <- trees$Distance.m > 0 &
                  trees$Distance.m <= 100

if (any(!valid_distance)) {
  stop("Error: Distance.m must be greater than 0 and at most 100.")
}

valid_angle <- trees$Angle.degrees > 0 &
               trees$Angle.degrees < 90

if (any(!valid_angle)) {
  stop("Error: Angle.degrees must be greater than 0 and less than 90.")
}

TreeHeight <- function(degrees, distance) {
  radians <- degrees * pi / 180
  height <- distance * tan(radians)
  return(height)
}

browser()

trees$height_m <- TreeHeight(
  trees$Angle.degrees,
  trees$Distance.m
)

input_basename <- basename(input_file)
output_file <- file.path(
  "results",
  paste0(sub("\\.csv$", "", input_basename), "_treeheights.csv")
)

dir.create("results", showWarnings = FALSE)
write.csv(trees, output_file, row.names = FALSE)