![img](https://miro.medium.com/v2/resize:fit:1400/1*iGdFJTHMIG79N2HChWaooQ.gif)

<center>

<h1>AutoBuddy</h1>

### **Chatbot for Customer Service and Vehicle Recommender**

---

</center>

<br />
<br />

## **Project Background**

Based on research conducted by Forbes, companies that use chatbots as a tool to interact with users see an average increase of 67 percent in revenue. Additionaly, according to a survey conducted by [Intercom](https://www.intercom.com/blog/the-state-of-chatbots/) with 500 business leaders, the use of chatbots can increase customer satisfaction by 24 percent.

According to research conducted by the website Kindly, chatbots can be a potential tool to use in increasing revenue because chatbots can improve customer experience, customer life time value (LTV), and average order value by providing 24/7 services in the form of product recommendations and customer service. This is especially true for e-commerce companies where according to research conducted by tidio, 77% of companies that successfully utilize chatbots are from e-commerce companies.

## **Objective**
Create a chatbot application (Virtual Shopping Assistance) that can provide 24/7 customer service and can provide product recommendations to increase revenue based on customer experience, LTV, and AOV variables.

## **Why Carsome?**

Carsome itself is Southeast Asia's largest integrated car e-commerce platform. We choose the brand because of it's commitment to digitalize used car industries in countries such as Malaysia, Indonesia, Thailand, and Singapore by reshaping and elevating the car buying and selling experience. Carsome provides end-to-end solutions to consumers and used car dealers, from car inspection to ownership transfer to financing, promising a service that is trusted, convenient and efficient.

## **Team Members**


1. [M. Fiqih Al-Ayubi](https://github.com/mfiqihalayubi) **(Data Engineer)**   
2. [Michael P.](https://github.com/mikepars) **(Data Scientist)**   
3. [Vicky Belario](https://github.com/vickybelario) **(Data Scientist)**   
4. [Ahmad Dani Rifai](https://github.com/dhans11) **(Data Analyst)**


## **Conclusion**

We created and tested 3 models, which is:
1. Base model (Using two separate model based on user prompt)
2. Retrieval Chain Method
3. Conversational Retrieval Chain

And based on the evaluation results, the model using the Conversational Retrieval Chain (CRC) method is the most superior and recommended for implementation as part of the Autobuddy chatbot.

<center>

---

![img](https://i.imgur.com/4GuLBBA.png)
#### Conversational Retrieval Chain (CRC) Workflow

---

</center>

This model offers high accuracy and the best performance in handling both FAQs and car recommendation questions. Adopting the CRC model is expected to significantly enhance the user experience on the Carsome platform.

## **Business Recommendation**

1. Increase the amount of FAQ data to improve the model's ability to answer specific questions related to administrative aspects.    
2. We would recommended to use stream processing methods to handle the data of cars sold on the platform so that the model can always receive updated data in real-time.

## **Room for Improvement**

1. Adding more features to the car dataset, such as user reviews, ratings, and historical sales data, can help the model provide more accurate and relevant recommendations.
2. Implementing deeper contextual understanding techniques, such as using transformer-based models like BERT.
3. Applying a feedback loop mechanism where users can provide direct feedback on the chatbot's answer quality, which can be used to continuously train and refine the model.

### [**Slide Project**](https://www.canva.com/design/DAGMqmQTmik/ZxsireTIhwfcg-_ITiN2sg/edit?utm_content=DAGMqmQTmik&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
### [**Dataset**](https://www.kaggle.com/datasets/indraputra21/used-car-listings-in-indonesia?select=used_car.csv)
### [**Deployment Demo**](https://drive.google.com/file/d/18srgZGhkPxruex62RCXlwg3URjR7Puq8/view?usp=sharing)
### [**Tableau**](https://public.tableau.com/app/profile/ahmad.dani.rifai/viz/CarListing_17223143129200/Dashboard1?publish=yes)
### [**Hugging Face**](https://huggingface.co/spaces/vickybelario/project01)
