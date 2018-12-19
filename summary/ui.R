library(rsconnect)
library(readr)
library(tidyverse)
library(shiny)
library(DT)
library(markdown)


shinyUI(fluidPage(

  # Application title
  titlePanel("Political Leaning Detector - Summary"),
    navbarPage(
      "",
      # Landing Page, Download
      tabPanel("Data",
         sidebarPanel(
           "Dataset Download", 
           br(),
           br(),
           downloadButton("downloadCoef", "Coefficents"),
           br(),
           br(),
           downloadButton("downloadCom", "All Comments (CSV)"),
           br(),
           br(),
           downloadButton("demJSON", "Demo Comments (JSON)"),
           br(),
           br(),
           downloadButton("repubJSON", "Repub Spreadsheet (JSON)"),
           width = 3
         ),
         mainPanel(
           includeMarkdown("landing.md")
         )
      ),
      # Landing Page, Download
      tabPanel("Coefficents",
        column(3,
          includeMarkdown("coef.md")
        ),
        column(4, 
          DT::dataTableOutput('coef')
       )
      ),
      # Comment Data Page
      tabPanel("Comments",
        DT::dataTableOutput('comments')
      )
    )
  )
)
