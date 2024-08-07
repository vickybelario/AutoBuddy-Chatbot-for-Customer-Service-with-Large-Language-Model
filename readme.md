![img](https://miro.medium.com/v2/resize:fit:1400/1*iGdFJTHMIG79N2HChWaooQ.gif)

<center>

<h1>AutoBuddy</h1>

### **Finetuned LLM Chatbot for Administrative and Vehicle Recommendation Questions for Carsome**

---

</center>

<br />
<br />

## **Project Background**

Based on research conducted by Forbes, companies that use chatbots as a tool to interact with users see an average increase of 67 percent in revenue. Additionaly, according to a survey conducted by [Intercom](https://www.intercom.com/blog/the-state-of-chatbots/) with 500 business leaders, the use of chatbots can increase customer satisfaction by 24 percent.

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

### [**Deployment Demo**](https://drive.google.com/file/d/18srgZGhkPxruex62RCXlwg3URjR7Puq8/view?usp=sharing)
### [**Tableau**](https://public.tableau.com/app/profile/ahmad.dani.rifai/viz/CarListing_17223143129200/Dashboard1?publish=yes)
### [**Hugging Face**](https://huggingface.co/spaces/vickybelario/project01)
