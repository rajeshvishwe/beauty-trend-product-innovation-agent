# ADK
terminal: adk web
url: http://127.0.0.1:8000 

## Start ui: 
terminal: python app.py

## Example :

1) What consumer problems do people have with everyday makeup?
2) Identify emerging everyday makeup opportunities and suggest a differentiated product concept for consumers who prefer lightweight, natural and multi-benefit beauty products.

## Architecture

```
                     User
                      │
                      ▼
             Innovation Brief
      ┌───────────────┼────────────────┐
      │               │                │
 Beauty Category  Target Audience  Target Market
                      │
               Business Question
                      │
                      ▼
                 Gradio UI
                      │
                      ▼
          Workflow Orchestration Service
                      │
                 ADK Runner
                      │
               In-Memory Sessions
                      │
                      ▼
            Trend Research Agent
                      │
                      ▼
              Serper Search Tool
                      │
                      ▼
          Google Search / Serper API
                      │
                      ▼
              Trend Intelligence
                      │
                      ▼
           Consumer Insight Agent
                      │
                      ▼
         Consumer Review Search Tool
                      │
                      ▼
              BeautyVectorStore
                      │
             Sentence Transformer
                      │
                      ▼
                    FAISS
                      │
          ┌───────────┴───────────┐
          │                       │
  Consumer Reviews CSV     Beauty Products CSV
          │                       │
          └───────────┬───────────┘
                      │
                      ▼
             Consumer Insights
                      │
                      ▼
      Competitor Intelligence Agent
                      │
                      ▼
              Serper Search Tool
                      │
                      ▼
           Competitor Intelligence
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
```

Trend Insights   Consumer Insights   Competitor Insights
│               │                │
└───────────────┴────────────────┘
│
            ▼
            Product Innovation Agent
            │
            ▼
            Innovative Product Concept
            │
            ▼
            Marketing Campaign Agent
            │
            ▼
            Campaign Recommendation
            │
            ┌─────────────────┼──────────────────┐
            │                 │                  │
            ▼                 ▼                  ▼
            Trend Intelligence  Product Concept  Campaign Strategy
            │                 │                  │
            └─────────────────┼──────────────────┘
            │
            ▼
            Executive Report Generator
            │
            Gemini
            │
            ▼
            Executive Innovation Report
            │
            ┌───────────┴───────────┐
            │                       │
            ▼                       ▼
            Gradio Results          Markdown Report
            Download File
