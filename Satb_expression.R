library(DESeq2)
library(ggplot2)
library(dplyr)
counts <- read.delim("GSE214654_featurecounts.count.gene.tsv.gz")
print(counts)

data1 <- counts
satb_genes <- c("SATB1", "SATB2")

satb_data1 <- data1 %>%
filter(grepl(paste(satb_genes, collapse = "|"), gene_id, ignore.case = TRUE))  

satb_data1

library(reshape2)
satb_data1_long <- melt(satb_data1, id.vars = "gene_id", variable.name = "Sample", value.name = "Expression")

ggplot(satb_data1_long, aes(x = Sample, y = Expression, fill = gene_id))+
  geom_bar(stat = "identity", position = "dodge")+
  theme(axis.title.x = element_text(angle = 0, hjust = 1 ))+
  theme(axis.text.x = element_text(angle = 90, hjust = 1))+
  labs(title = "SATB Gene Expression in Data1", x = "Sample" , y = "Expression")
