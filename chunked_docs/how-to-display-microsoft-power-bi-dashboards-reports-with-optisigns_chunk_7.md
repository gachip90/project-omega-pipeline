# How to Display Microsoft Power BI Dashboards & Reports with OptiSigns

## Add Power BI App on OptiSigns

Now, it's time to add an instance of the Power BI app to your OptiSigns account.

Navigate to the [**OptiSigns Portal**](https://app.optisigns.com/)**,**then click **Files/Assets** → **Apps**.

![optisigns files assets apps](https://support.optisigns.com/hc/article_attachments/37495309686163)

Navigate to the **Power BI app**.

![optisigns power bi app location](https://support.optisigns.com/hc/article_attachments/37495309693203)

Enter your Power BI app details.

![](https://support.optisigns.com/hc/article_attachments/44002355209107)

* **Name -** Name of your Power BI app instance. This is the name of the app in your asset list. It will **not** be displayed on your screens.
* **URL -**  Paste in the Dashboard URL you copied in Step 1 here.
* **Update Interval -** Select how often you want the app to check for an update to the Dashboard. The Default is 600 seconds (10 minutes).
* **Use Service Principal -** When selected, uses a Microsoft Entra ID Service Principal to log in to Power BI. This requires additional setup. For more information, see [How to Set Up a Power BI Service Principal for Use with OptiSigns](https://support.optisigns.com/hc/en-us/articles/32860569148819-How-to-Set-Up-a-PowerBI-Service-Principal-for-Use-in-OptiSigns).
  + **Select the "User Service Principal" Integration** - Where you choose the service principal integration for your Power BI reports.
* **Direct Login -** In order to view your dashboard on any screen, OptiSigns requires you to authenticate via the pass-through to Microsoft's Power BI service. Simply input your Microsoft ID and password.

Once you've integrated a Service Principal or directly logged in, you're ready to display. On the right is the **Preview** pane. If you've set up your report correctly, you should see it display here. You can change its orientation by switching between **Landscape** and **Portrait**.

|  |
| --- |
| **NOTE** |
| A successful Preview will prove that your Power BI report has properly integrated with OptiSigns. However, it **DOES NOT** mean that it will display on your screen the same way. A variety of additional factors can affect how your Power BI displays, including (but not limited to):   * Type of device being used to display * Device memory * Reliability of network connection * Company firewalls and other network restrictions   If you're still having trouble getting your Power BI reports to display after all these have been accounted for, please contact us at [support@optisigns.com](mailto:support@optisigns.com). |

If it appears to your satisfaction, you can choose to assign your Power BI app instance either directly to a screen or as part of a [Playlist](https://support.optisigns.com/hc/en-us/articles/28295104605843-How-to-Create-Use-Playlists) and/or [Schedule](https://support.optisigns.com/hc/en-us/articles/360016981853-Create-and-Using-Schedules-with-OptiSigns).

This instance will display a single page of a report. You will need to create multiple instances to show multiple pages of a report. These can be placed into a Playlist to have a constantly rotating series of slides showing entire reports or dashboards, or sprinkled in with other Assets - however you like.




---
Article URL: https://support.optisigns.com/hc/en-us/articles/360024859713-How-to-Display-Microsoft-Power-BI-Dashboards-Reports-with-OptiSigns