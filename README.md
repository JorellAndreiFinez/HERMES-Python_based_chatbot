# ⚙️ Hermes – Smart Personal Assistant for Common Tasks

> **A Python-based desktop assistant that automates predefined tasks through an intuitive, user-friendly interface.**
> Developed as part of the **Integrative Programming and Technologies (IT0011)** course under the **Department of Information Technology**, TW24.

---

## 🧭 Overview

**Hermes** is a Python-based personal assistant designed to simplify daily computing tasks through a clean, responsive interface.
Created by a team of BSIT students from TW24, this project was submitted to **Dr. Roman De Angel** on **March 31, 2024**, for the course *Integrative Programming and Technologies (IT0011)*.

The system was developed under **Jorell Andrei P. Finez** — serving as **Project Manager** and **Lead Developer** — along with Larry Louie Lacandazo, Markiel Andrei Leones, and Julia Ansherina Mendoza.

Inspired by **Hermes**, the messenger of the Greek gods, this project represents **speed, adaptability, and reliability** in helping users manage their digital tasks efficiently.

---

## 🧩 Project Rationale

In today’s fast-paced digital environment, users juggle multiple tasks and data sources. While existing assistants like Siri and Alexa provide automation, they often depend on online services or complex integrations.

**Hermes** bridges this gap with an **offline, modular desktop assistant** that performs common tasks — such as chatting, storing notes, managing reminders, and solving basic computations — through a structured, predefined logic system.

It’s a practical demonstration of **integrative programming**, combining Python modules, GUI frameworks, and logical workflows into a cohesive, user-centered application.

---

## 🎯 Project Objectives

The Hermes project aims to develop an personal assistant capable of performing a wide range of interactive and administrative tasks. Specifically, the objectives are to:

1. Enhance user interaction through conversational features such as mood-based responses, quotes, jokes, and activity suggestions.

2. Implement robust user management, enabling administrators to create, update, delete, and display user accounts securely through a dedicated admin interface.

3. Support CRUD operations for user-generated content, including notes, reminders, and bookmarks, ensuring efficient data handling and accessibility.

4. Incorporate computational capabilities, allowing users to perform arithmetic and math-related commands directly within the chatbot.

5. Strengthen data security and integrity using JSON-based local storage to safeguard user information and maintain offline functionality.

6. Improve user experience and engagement through responsive UI design, adaptive chatbot behavior, and informative responses.

7. Demonstrate integrative programming principles by combining multiple Python modules, GUI frameworks, and logical structures into a cohesive, intelligent desktop application.

---

## 🧠 Core Features

### 👤 User & Admin Management

* Create, update, and delete user profiles.
* Secure JSON-based data storage with password validation.
* Admin-level account management and overview functions.

### 💬 Chatbot & Task Assistant

* Handles predefined queries and conversational prompts.
* Supports math computations and dictionary lookups.
* Generates random jokes, quotes, and compliments.
* Responds dynamically based on user mood.

### 🗂️ Notes & Reminders

* CRUD operations for user notes and scheduled reminders.
* Bookmark system for frequently used terms.
* Data stored locally for fast and private access.

### 🧮 Utility Tools

* **Sympy** for arithmetic and symbolic math.
* **PyDictionary** for word meaning and synonym retrieval.
* **Datetime** and **threading** for reminders and background tasks.

---

## 🖥️ User Interface Overview

The following screenshots showcase key interfaces and functionalities of **HermesPy**, highlighting its user-friendly design and intelligent chatbot interactions.

### 🧭 Startup
- **Start Screen** – Displays the HermesPy logo and navigation options for login or signup.
  
  ![HermesPy Chat Interface](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-login.png)

### ⚙️ Admin Dashboard
- **Account Management** – Admins can create, update, delete, and view individual or all user accounts with real-time confirmation feedback.
  
    ![HermesPy Chat Interface](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-admin%20account.png)

### 💬 Chatbot Interface
- **Main Chat Window** – The interactive space where users can engage with HermesPy using natural language commands.

  ![HermesPy Chat Interface](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20window.png)
    
- **Help Command** – Displays a complete list of supported commands for easy reference..

  ![HermesPy Chat Interface](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20help.png)
    
- **Interactive Responses** – HermesPy offers dynamic replies to greetings, questions, and casual conversations, adding personality and engagement..

  ![HermesPy Chat Interface](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20response%201.png)
  ![HermesPy Chat Interface](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20response%202.png)

### 🧾 Smart Functionalities

#### 🗓️ Reminders & Notes  
Users can add, view, update, or delete reminders and notes directly from chat commands.  

![HermesPy Reminders 1](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20reminders%201.png)
![HermesPy Reminders 2](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20reminders%202.png)
![HermesPy Reminders 3](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20reminders%203.png)
![HermesPy Reminders 4](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20reminders%204.png)
![HermesPy Reminders 5](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20reminders%205.png) 

#### 🔖 Bookmarks  
Save and retrieve important words or phrases for future reference.  

![HermesPy Bookmark 1](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20bookmark%201.png)
![HermesPy Bookmark 2](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20bookmark%202.png)


#### 🔍 Information Queries  
Ask HermesPy for definitions, quotes, fun facts, or activity suggestions.  

![HermesPy Info 1](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20info%201.png)
![HermesPy Info 2](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20info%202.png)
![HermesPy Info 3](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20info%203.png)
![HermesPy Info 4](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20info%204.png)
![HermesPy Info 5](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20info%205.png)
![HermesPy Info 6](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20info%206.png)
![HermesPy Info 7](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20info%207.png)

#### 🧮 Utilities  
Perform calculations, request the current time, or clear chat history with simple commands.  

![HermesPy Utility 1](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20util%201.png)
![HermesPy Utility 2](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20util%202.png)
![HermesPy Utility 3](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20util%203.png)
![HermesPy Utility 4](https://fucdounsdyfahuicxpls.supabase.co/storage/v1/object/public/HERMES/hermes-chat%20util%204.png)

  
---

## 🧩 Technologies

| Library / Module          | Purpose                              |
| ------------------------- | ------------------------------------ |
| **tkinter, ttkbootstrap** | GUI and theme design                 |
| **json, os**              | Local data storage and file handling |
| **threading**             | Concurrent background operations     |
| **random**                | Dynamic responses and interactions   |
| **sympy**                 | Mathematical computations            |
| **pydictionary**          | Word definition and synonyms         |
| **datetime, time**        | Time-based reminders and utilities   |
| **PIL (Pillow)**          | Image rendering                      |
| **pyglet**                | Font and multimedia integration      |
| **re**                    | Input validation and formatting      |

---

## 🧩 Development Objectives

1. Implement secure user and admin management modules.
2. Enable note, reminder, and data CRUD functionality.
3. Integrate chatbot features using predefined logic.
4. Design a responsive interface with **ttkbootstrap**.
5. Ensure offline usability for accessibility and performance.

---

## 🏆 Project Team

Submitted by:

- Finez, Jorell Andrei
- Lacandazo, Larry
- Leones, Markiel Andrei
- Mendoza, Julia Ansherina


Submitted to:

**Dr. Roman De Angel**
Department of Information Technology  
FEU Institute of Technology 

> Integrative Programming and Technologies (IT0011)
> Submission Date: March 31, 2024

---

## 🔗 Related Links  

- [Hermes Official Documentation](https://drive.google.com/file/d/1UmsBXe3_X1zdWnI-xCMYx_8xfKwexSon/view?usp=sharing)  
- [Hermes Documentation Explanation](https://drive.google.com/file/d/11lSuwaIFbO_zMLk_SdQ_FipI-q-GXJq-/view?usp=sharing)

---

## 📜 License

This project is licensed under the **MIT License** — open for educational and personal use.

---

> “Efficiency through simplicity — Hermes helps you focus on what matters most.”
