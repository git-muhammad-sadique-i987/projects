<img src="https://cdn.prod.website-files.com/677c400686e724409a5a7409/6790ad949cf622dc8dcd9fe4_nextwork-logo-leather.svg" alt="NextWork" width="300" />

# P1 - Build a Chatbot with Amazon Lex

**Project Link:** [View Project](http://learn.nextwork.org/projects/aws-ai-lex1)

**Author:** Muhammad Sadique  
**Email:** saddi2u@gmail.com

---

## Build a Chatbot with Amazon Lex

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-ai-lex1_505be5b8)

---

## Introducing Today's Project!

### What is Amazon Lex?

Amazon Lex is an AI service for building conversational interfaces using voice and text. It’s useful for creating chatbots, virtual assistants, and voice applications, enabling automated customer interactions/ support, and enhancing user experience.

### How I used Amazon Lex in this project

I have used Amazon Lex in this project to take on role of Banking Bot which can recognise the intent and utterance of user and welcome it accordingly.

### One thing I didn't expect in this project was...

I did'nt expected variations to be there. Also i did'nt expected voice recogition and sound reply by Amazon Lex.

### This project took me...

90 minuts.

---

## Setting up a Lex chatbot

I created my chatbot from scratch with Amazon Lex. Setting it up took me 2 minutes. Really easy to setup.

While creating my chatbot, I also created a role with basic permissions because Amazon Lex needs the permission to call other AWS services on user's behalf. Later in this project series I'll be integrating Lex with another service called Lambda.

In terms of the intent classification confidence score, I kept the default value of 0.40. This means chatbot needs to be at least 40% confident that it understands what the user is asking to be able to give a response.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-ai-lex1_97dc2351)

---

## Intents

Intents are what the user is trying to achieve in their conversation with the chatbot. For example, checking a bank account balance; booking a flight; ordering food.

If you set up different intents, one single chatbot can manage a bunch of requests.

I created my first intent, WelcomeIntent, to greet or weclome users as part of initiation of converstation.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-ai-lex1_505be5b8)

---

## FallbackIntent

I launched and tested my chatbot, which could respond successfully if I enter: "Hi", or "I need help" etc.

My chatbot returned the error message 'Intent FallbackIntent is fulfilled' when I entered "Good Morning" This error message occurred because the chatbot could'nt recognize my intent/ utterance hence it shown error.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-ai-lex1_505be5b8)

---

## Configuring FallbackIntent

FallbackIntent is a default intent in every chatbot that gets triggered when your chatbot has a confidence score below the set value (in this case 40%) for all the intents you've defined.  


I wanted to configure FallbackIntent so that it displays a custom message to the user if it does not understand the user input.

---

## Variations

To configure FallbackIntent, I clicked left hand navigation panel, choose FallbackIntent. 
Scroll down to Closing responses.

Expand the arrow for Response sent to the user after the intent is fulfilled.

I then added the desired message in the edit.

I also added variations! For an end user, it is an alternative of the same Message. When Amazon Lex needs to return a Fallback response, it will randomly choose a message from the group and return that, making the response more conversational.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-ai-lex1_c4fc89af)

---

## Initial Responses

As an extension for this project, I'm setting up initial responses, which are "Hmmm this is interesting...", "One moment..."
I've set up initial responses for giving our users a heads up about what to expect.

The initial response messages I set up are "Hmmm this is interesting...", "One moment..."
I've set up initial responses for giving our users a heads up about what to expect.

![Image](http://learn.nextwork.org/thankful_brown_optimistic_cobra/uploads/aws-ai-lex1_09bcb9701)

---

---
