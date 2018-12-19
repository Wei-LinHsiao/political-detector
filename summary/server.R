library(rsconnect)
library(shiny)
library(readr)
library(tidyverse)
library(DT)

# Import data
coef <- read.csv("coef.csv", header=FALSE)
comments <- read.csv("comments.csv")

# Add title to coefficents
colnames(coef) <- c("Phrase", "Coefficent")

# Adjust last column to UNIX timestamp column
comments <- comments %>% mutate(Timestamp = as.POSIXct(Timestamp, origin="1970-01-01", tz = "UTC"))


shinyServer(function(input, output) {
  # Table for comments
  output$comments <- DT::renderDataTable(
    DT::datatable(comments)
  )
  
  # Table for coefficents
  output$coef <- DT::renderDataTable(
    DT::datatable(coef)
  )
  
  # Files for downloading
  output$downloadCoef<- downloadHandler(
    filename = function() {
      "pol_detect_coeff.csv"
    },
    content = function(file) {
      write.csv(coef, file, row.names = FALSE)
  })
  
  # Comments
  output$downloadCom<- downloadHandler(
    filename = function() {
      "pol_detect_reddit_comments.csv"
    },
    content = function(file) {
      write.csv(comments, file, row.names = FALSE)
  })
  
  # Differnt spreadsheet for Republicans and Democrats
  output$demJSON <- downloadHandler(
    filename = "data_demo_full.json",
    content = function(file) {
      file.copy("data_demo_full.json", file)
    })
  
  output$repubJSON <- downloadHandler(
    filename = "data_repub_full.json",
    content = function(file) {
      file.copy("data_repub_full.json", file)
    })
})
