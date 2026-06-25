# How to Display Microsoft Power BI Dashboards & Reports with OptiSigns

### Creating a Filter to Automatically Target Certain Screens (Optional)

By pairing these filters with OptiSigns [**Device Additional Attributes**](https://support.optisigns.com/hc/en-us/articles/360048914673-Edit-Screen-What-does-each-option-do#attributes), it is possible to apply them only to certain screens. This is useful if you have multiple screen locations, for example, and only wish to show Power BI data which is relevant to them.

To set this up, navigate to the **Device Additional Attributes** by editing your screen. This can be found through the **Screens tab,** then finding the screen you wish to Edit. Click **Edit Screen → Advanced → More → Device Additional Attributes**.  
![](https://support.optisigns.com/hc/article_attachments/44002355241875)

Here’s where it gets fun. On the Device Additional Attributes screen, you’ll see two fields: **Key**, and **Value**.

![](https://support.optisigns.com/hc/article_attachments/44002377564179)

* **Key** - A parameter that will be used by the filter. This will replace either the Table, Column, or Value, as you’ll see in a moment. You’ll want to keep your Key consistent across ALL screens where you plan to display a filtered Power BI report.
* **Value** - Dictates which part of the report to share with this screen. You’ll want this to vary depending on the screen.

For this example, we will fill in the Key as **Location** and the Value as **Central**:

![](https://support.optisigns.com/hc/article_attachments/44002355249939)

For practical purposes, what we’re saying here is that this screen’s Location is in the Central region, which corresponds to the Values which exist on our Power BI report. You can add as many attributes to an individual screen as you wish.

|  |
| --- |
| **IMPORTANT** |
| The Value here MUST match up with an element of your report if you wish to apply the filter properly. In our example report, we have Central, East, and West, so one of these must be the value for the report to display properly. Your report will be different. |

Now that we’ve set this up, we can return to our Power BI report. Now, we’ll substitute the **Value** for **{{Location}}**:

![](https://support.optisigns.com/hc/article_attachments/44002377569939)

By inputting this and assigning this to a screen, it will find the Device Additional Attribute and substitute the Value here. In this case, that value is Central, so it will filter out all data that does not fall under the Account Table, Region Column, and Central Value.

For a different screen, you might set the Device Additional Attribute value to East. By pairing this same report to that screen, it will filter out all data that does not fall under the Account Table, Region Column, and East value.

Let’s see how this works with a practical example:

* Say we have 3 screens in 3 locations:
  + Screen A is in Location 1, Screen B is in Location 2, and Screen C is in Location 3
* We only want these screens to show the appropriate data off this report
  + On each screen, we go to Device Additional Attributes. We set Key as Location and the Value as Location 1 for Screen A; Location 2 for B; and Location 3 for C
  + We set the Value in our Power BI report to {{Location}}
* It will automatically filter the report based on the device’s set location, and this app can be used across all 3 screens and will show different data depending on where the screen is located

Pretty cool, huh? This can also be used to replace the Table or Column values depending on your use case or need.



---
Article URL: https://support.optisigns.com/hc/en-us/articles/360024859713-How-to-Display-Microsoft-Power-BI-Dashboards-Reports-with-OptiSigns