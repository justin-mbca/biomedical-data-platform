# DESeq2 analysis (from bioinformatics_pipeline)
# Placeholder: creates dummy results for pipeline demo
# Production: run full DESeq2 workflow with design matrix

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 3) {
  in_file <- "results/counts_for_deseq2.csv"
  out_results <- "results/deseq2_results.csv"
  out_ma <- "results/deseq2_MAplot.png"
} else {
  in_file <- args[1]
  out_results <- args[2]
  out_ma <- args[3]
}

counts <- read.csv(in_file, row.names = 1)
n_genes <- nrow(counts)
# Placeholder: random log2FC and pvalues for demo
set.seed(42)
deseq2_results <- data.frame(
  gene_id = rownames(counts),
  baseMean = rowMeans(counts),
  log2FoldChange = rnorm(n_genes, 0, 1),
  lfcSE = runif(n_genes, 0.1, 0.5),
  pvalue = runif(n_genes, 0.001, 0.5)
)
write.csv(deseq2_results, out_results, row.names = FALSE)
# Dummy MA plot
png(out_ma, width = 400, height = 400)
plot(deseq2_results$baseMean, deseq2_results$log2FoldChange, pch = 19, col = "grey", main = "MA Plot")
dev.off()
message("DESeq2 results saved to ", out_results)
