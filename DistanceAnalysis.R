library("dplyr")
library("tidyr")
library("ggplot2")
library("stringr")
library("rstatix")
library("ggpubr")

fileList <- list.files(pattern = "MainChainDistanceMatrix.txt")

df <- matrix(ncol = 8, nrow = 0) %>%
  as.data.frame()

for (FILE in fileList) {
  
  x <- read.delim(file = FILE, 
                  sep = "\t", header = FALSE) %>%
    matrix(nrow = 60, ncol = 60, byrow = TRUE) %>%
    as.data.frame()
  
  rownames(x) <- c(1:60) %>% as.character()
  colnames(x) <- c(1:60) %>% as.character()
  
  x <- x %>%
    mutate(Residue1 = rownames(.)) %>%
    pivot_longer(!Residue1, names_to = "Residue2", values_to = "Distance") %>%
    mutate(Residue1 = as.numeric(Residue1), 
           Residue2 = as.numeric(Residue2)) %>%
    mutate(Distance = unlist(Distance)) %>%
    mutate(Helix_Residue1 = case_when(Residue1 %in% c(10:22) ~ "Helix1", 
                                      Residue1 %in% c(27:37) ~ "Helix2",
                                      Residue1 %in% c(42:56) ~ "Helix3")) %>%
    mutate(Helix_Residue2 = case_when(Residue2 %in% c(10:22) ~ "Helix1", 
                                      Residue2 %in% c(27:38) ~ "Helix2",
                                      Residue2 %in% c(42:56) ~ "Helix3")) %>%
    mutate(name = str_split_1(FILE, pattern = "_") %>% .[1])
  
  nonExistentResidues <- x %>%
    group_by(Residue1) %>%
    summarize(total = sum(Distance)) %>%
    filter(total == 0) %>%
    .$Residue1
  
  print(FILE)
  print(nonExistentResidues)
  
  x <- x %>% 
    filter( !(Residue1 %in% nonExistentResidues)) %>%
    filter( !(Residue2 %in% nonExistentResidues))
  
  df <- rbind(df, x)
  
  
}

df <- df %>%
  mutate(Type = case_when(name %in% c("1HDD", "1ig7", "8eml", "4rdu", "8pmc") ~ "ANTP", 
                          TRUE ~ "Paired-like"))


H <- data.frame(xmin = c(9.5, 27.5, 41.5), 
                xmax = c(22.5, 37.5, 56.5), 
                ymin = c(1,1,1), 
                ymax = c(60,60,60))



specificPairs <- df %>%
  mutate(Pair = paste(Residue1, Residue2, sep = " - ")) %>%
  filter(Pair %in% c("12 - 38",
                     "15 - 34", 
                     "19 - 30", 
                     "22 - 29", 
                     "13 - 48", 
                     #"16 - 45", 
                     "17 - 52", 
                     #"20 - 49",
                     "31 - 42",
                     #"28 - 46", 
                     #"35 - 42", 
                     "34 - 45")) %>%
  mutate(Pair = factor(Pair, 
                       levels = c("12 - 38",
                                  "15 - 34", 
                                  "19 - 30", 
                                  "22 - 29", 
                                  "13 - 48", 
                                  #"16 - 45", 
                                  "17 - 52", 
                                  #"20 - 49", 
                                  "31 - 42",
                                  #"28 - 46", 
                                  #"35 - 42", 
                                  "34 - 45"),
                       ordered = TRUE)) %>%
  mutate(HelixCombo = case_when(Pair %in% c("12 - 38",
                                            "15 - 34", 
                                            "19 - 30", 
                                            "22 - 29") ~ "Helix 1 & Helix 2", 
                                Pair %in% c("13 - 48", 
                                            "16 - 45", 
                                            "17 - 52", 
                                            "20 - 49") ~ "Helix 1 & Helix 3", 
                                Pair %in% c( "31 - 42",
                                             "28 - 46", 
                                             "35 - 42", 
                                             "34 - 45") ~ "Helix 2 & Helix 3", 
                                TRUE ~ NA))

stats <- specificPairs %>%
  group_by(Pair) %>%
  t_test(Distance ~ Type) %>%
  add_xy_position() %>%
  mutate(p.adj = p.adjust(p, method = "holm"))

specificPairs %>%
  mutate(Type = factor(Type, 
                       levels = c("Paired-like", "ANTP"),
                       ordered = TRUE)) %>% 
  ggplot(aes(x = Type, 
             y = Distance, 
             fill = Type, 
             color = Type,
             # ymin = Distance - Distance.SD, 
             # ymax = Distance + Distance.SD
             )) + 
  geom_boxplot(alpha = 0.3) + 
  xlab("Homeodomain class") + 
  ylab("Distance between\nalpha carbons (Å)") + 
  stat_pvalue_manual(stats, 
                     inherit.aes = FALSE, 
                     tip.length = 0) + 
  facet_wrap(~Pair, nrow = 1) + 
  scale_y_continuous(expand = c(0, 1)) + 
  scale_fill_manual(values = c("#A02B93", "#4EA72E")) + 
  scale_color_manual(values = c("#A02B93", "#4EA72E")) + 
  theme_bw() + 
  theme(text = element_text(size = 15), 
        axis.text.x = element_text(angle = 30, 
                                   hjust = 1, 
                                   vjust = 1), 
        legend.position = "bottom", 
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(),
        plot.title = element_text(hjust = 0.5))


summ <- df %>%
  group_by(Residue1, Residue2, Type) %>%
  summarize(DistanceMean = mean(Distance, na.rm = TRUE)) %>%
  pivot_wider(names_from = "Type", values_from = "DistanceMean") %>%
  mutate(Delta = `Paired-like` - ANTP)

summ %>%
  ggplot(aes(x = Residue1, 
             y = Residue2, 
             fill = Delta)) + 
  geom_tile() + 
  scale_fill_gradient2(mid = "white", 
                       high = "cornflowerblue", 
                       low = "darkorange3", 
                       midpoint = 0, 
                       limits = c(-2, 2), 
                       oob = scales::squish, 
                       name = "") + 
  scale_x_continuous(n.breaks = 12, 
                     limits = c(0,60), 
                     expand = c(0,0)) + 
  scale_y_continuous(n.breaks = 12, 
                     limits = c(0,60), 
                     expand = c(0,0)) + 
  xlab("Residue 1") + 
  ylab("Residue 2") + 
  ggtitle("Paired-like minus ANTP main chain distances (Å)") + 
  theme_bw() +
  theme(text = element_text(size = 24), 
        plot.title = element_text(size = 20),
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank())


