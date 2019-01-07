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
         
         mainPanel(
           column(
            includeMarkdown("landing.md"),
            width = 8
           ),
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
             downloadButton("demJSON", "D Comments (JSON)"),
             br(),
             br(),
             downloadButton("repubJSON", "R Comments (JSON)"),
             width = 4
           )
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
