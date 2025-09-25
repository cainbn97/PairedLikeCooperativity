library("tidyr")
library("ggplot2")
library("dplyr")
library("stringr")

## ALX4 transposed on EN1 ##
x <- read.delim(file = "StericOverlapCalculations/9D9Rw1HDD_helicalSpacing_ResidueOverlap.txt", 
                header = FALSE)

matrix <- x  %>% matrix(ncol = 66, byrow = TRUE) %>%
  as.data.frame()

rownames(matrix) <- c(-3:64) %>% as.character()
colnames(matrix) <- c(0:65) %>% as.character()


df <- matrix %>%
  mutate(Residue1 = rownames(.)) %>%
  pivot_longer(!Residue1, 
               names_to = "Residue2", 
               values_to = "AreaOverlap") %>%
  mutate(AreaOverlap = unlist(AreaOverlap)) 


Residue1Clash <- df %>%
  ## Residues with predicted Hbonds
  #filter( !((Residue1 == 0) & (Residue2 == 25))  ) %>%
  filter( !((Residue1 == 0) & (Residue2 == 28))  ) %>%
  filter( !((Residue1 == 3) & (Residue2 == 42))  ) %>%
  filter( !((Residue1 == 25) & (Residue2 == 2))  ) %>%
  filter( !((Residue1 == 28) & (Residue2 == 2))  ) %>%
  mutate(Residue = as.numeric(Residue1), 
         Chain = 1) %>%
  group_by(Residue, Chain) %>%
  summarize(Sum = sum(AreaOverlap))

Residue2Clash <- df %>%
  ## Residues with predicted Hbonds
  #filter( !((Residue1 == 0) & (Residue2 == 25))  ) %>%
  filter( !((Residue1 == 0) & (Residue2 == 28))  ) %>%
  filter( !((Residue1 == 3) & (Residue2 == 42))  ) %>%
  filter( !((Residue1 == 25) & (Residue2 == 2))  ) %>%
  filter( !((Residue1 == 28) & (Residue2 == 2))  ) %>%
  mutate(Residue = as.numeric(Residue2), 
         Chain = 2) %>%
  group_by(Residue, Chain) %>%
  summarize(Sum = sum(AreaOverlap))

Residueclash_transposedALX4 <- rbind(Residue1Clash, 
                      Residue2Clash) %>%
  mutate(Structure = "ALX4 dimer with Engrailed helical spacing")

## ALX4 dimer ##

x <- read.delim(file = "StericOverlapCalculations/9D9R_ResidueOverlap.txt", 
                header = FALSE)

matrix <- x  %>% matrix(ncol = 66, byrow = TRUE) %>%
  as.data.frame()

rownames(matrix) <- c(210:277) %>% as.character()
colnames(matrix) <- c(213:278) %>% as.character()


df <- matrix %>%
  mutate(Residue1 = rownames(.)) %>%
  pivot_longer(!Residue1, 
               names_to = "Residue2", 
               values_to = "AreaOverlap") %>%
  mutate(Residue1 = as.numeric(Residue1) - 213) %>%
  mutate(Residue2 = as.numeric(Residue2) - 213) %>%
  mutate(AreaOverlap = unlist(AreaOverlap)) 


Residue1Clash <- df %>%
  ## Residues with predicted Hbonds
  filter( !((Residue1 == 3) & (Residue2 == 42))  ) %>%
  filter( !((Residue1 == 1) & (Residue2 == 28))  ) %>%
  filter( !((Residue1 == 0) & (Residue2 == 25))  ) %>%
  filter( !((Residue1 == 0) & (Residue2 == 23))  ) %>%
  filter( !((Residue1 == 25) & (Residue2 == 2))  ) %>%
  filter( !((Residue1 == 28) & (Residue2 == 2))  ) %>%
  mutate(Residue = as.numeric(Residue1), 
         Chain = 1) %>%
  group_by(Residue, Chain) %>%
  summarize(Sum = sum(AreaOverlap))

Residue2Clash <- df %>%
  ## Residues with predicted Hbonds
  filter( !((Residue1 == 3) & (Residue2 == 42))  ) %>%
  filter( !((Residue1 == 1) & (Residue2 == 28))  ) %>%
  filter( !((Residue1 == 0) & (Residue2 == 25))  ) %>%
  filter( !((Residue1 == 0) & (Residue2 == 23))  ) %>%
  filter( !((Residue1 == 25) & (Residue2 == 2))  ) %>%
  filter( !((Residue1 == 28) & (Residue2 == 2))  ) %>%
  mutate(Residue = as.numeric(Residue2), 
         Chain = 2) %>%
  group_by(Residue, Chain) %>%
  summarize(Sum = sum(AreaOverlap))

Residueclash_ALX4Dimer <- rbind(Residue1Clash, 
                      Residue2Clash) %>%
  mutate(Structure = "ALX4 dimer")


## Engrailed docked on the P3 site
x <- read.delim(file = "StericOverlapCalculations/EnDockedonP3_ResidueOverlap.txt", 
                header = FALSE)

matrix <- x  %>% matrix(ncol = 57, byrow = TRUE) %>%
  as.data.frame()

rownames(matrix) <- c(3:59) %>% as.character()
colnames(matrix) <- c(3:59) %>% as.character()


df <- matrix %>%
  mutate(Residue1 = rownames(.)) %>%
  pivot_longer(!Residue1, 
               names_to = "Residue2", 
               values_to = "AreaOverlap") %>%
  mutate(AreaOverlap = unlist(AreaOverlap)) 


Residue1Clash <- df %>%
  ## Residues with predicted Hbonds
  mutate(Residue = as.numeric(Residue1), 
         Chain = 1) %>%
  group_by(Residue, Chain) %>%
  summarize(Sum = sum(AreaOverlap))

Residue2Clash <- df %>%
  ## Residues with predicted Hbonds
  mutate(Residue = as.numeric(Residue2), 
         Chain = 2) %>%
  group_by(Residue, Chain) %>%
  summarize(Sum = sum(AreaOverlap))

Residueclash_EngrailedDocked <- rbind(Residue1Clash, 
                                     Residue2Clash) %>%
  mutate(Structure = "Engrailed docked on P3 site")



####################### PLOTS ############################

Residueclash <- rbind(Residueclash_ALX4Dimer,
                      Residueclash_transposedALX4, 
                      Residueclash_EngrailedDocked)

Residueclash %>%
  mutate(Chain = factor(Chain, 
                        levels = c(2, 1), 
                        ordered = TRUE)) %>%
  ggplot(aes(x = Residue, 
         y = Chain, 
         fill = Sum)) + 
  geom_tile(color = "lightgray", 
            linewidth = 0.8) + 
  scale_fill_gradient(low = "white",
                      high = "brown2", 
                      #transform = "log2", 
                      na.value = "#DCEAF7", 
                      #limits = c(-0.3, 50), 
                      oob = scales::squish,
                      name = ""
                        #expression(paste("Surface Area\nOverlap \n(", ring(A)^2,")    ", sep = ""))
                      ) + 
  scale_x_continuous(breaks = seq(by = 5, to = 65, from = 0), 
                     limits = c(-3, 65), 
                     expand = c(0,0.5)) + 
  facet_wrap(~Structure, nrow = 4) + 
  xlab("DNA binding domain position") + 
  theme_bw() + 
  theme(text = element_text(size = 24), 
        strip.text.x.top = element_text(size = 18, hjust = 0),
        axis.title = element_text(size = 20),
        strip.background.x = element_blank(),
        panel.grid.minor = element_blank(), 
        panel.grid.major = element_blank(), 
        panel.spacing = unit(1, "lines"), 
        panel.border = element_blank(), 
        #legend.position = "bottom", 
        legend.key.height = unit(1, 'cm'), 
        axis.ticks.y = element_blank())

