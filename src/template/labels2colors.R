 labels2colors <- function (labels, zeroIsGrey = TRUE, colorSeq = NULL, naColor = "grey", 
  commonColorCode = TRUE) 
{
  if (is.null(colorSeq)) 
    colorSeq = standardColors()
  if (is.numeric(labels)) {
    if (zeroIsGrey) 
      minLabel = 0
    else minLabel = 1
    if (any(labels < 0, na.rm = TRUE)) 
      minLabel = min(c(labels), na.rm = TRUE)
    nLabels = labels
  }
  else {
    if (commonColorCode) {
      factors = factor(c(as.matrix(as.data.frame(labels))))
      nLabels = as.numeric(factors)
      dim(nLabels) = dim(labels)
    }
    else {
      labels = as.matrix(as.data.frame(labels))
      factors = list()
      for (c in 1:ncol(labels)) factors[[c]] = factor(labels[, 
        c])
      nLabels = sapply(factors, as.numeric)
    }
  }
  if (max(nLabels, na.rm = TRUE) > length(colorSeq)) {
    nRepeats = as.integer((max(labels) - 1)/length(colorSeq)) + 
      1
    warning(paste("labels2colors: Number of labels exceeds number of avilable colors.", 
      "Some colors will be repeated", nRepeats, "times."))
    extColorSeq = colorSeq
    for (rep in 1:nRepeats) extColorSeq = c(extColorSeq, 
      paste(colorSeq, ".", rep, sep = ""))
  }
  else {
    nRepeats = 1
    extColorSeq = colorSeq
  }
  colors = rep("grey", length(nLabels))
  fin = !is.na(nLabels)
  colors[!fin] = naColor
  finLabels = nLabels[fin]
  colors[fin][finLabels != 0] = extColorSeq[finLabels[finLabels != 
    0]]
  if (!is.null(dim(labels))) 
    dim(colors) = dim(labels)
  colors
}

