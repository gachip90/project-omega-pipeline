# How to Display Microsoft Power BI Dashboards & Reports with OptiSigns

## Frequently Asked Questions

#### **How does security work with OptiSigns Power BI integration?**

OptiSigns integrates with and displays Power BI dashboards via an official Microsoft API, securely integrated through your Power BI or MS Azure portal. No usernames or passwords are stored in OptiSigns.

Your devices (screens) will display your Power BI report on the screens directly. Power BI data does not pass through our servers. There is no data-farming on our end of any kind.

OptiSigns uses Microsoft APIs for integration. In order for our integrations to work, the integration has to be approved by an administrator. This is the same across all integrations using Microsoft APIs.

This administrator access is only needed for first time access. Once the OptiSigns app is approved for use, other users can use OptiSigns directly.

Customers with MS Azure Enterprise Apps management can also [manage OptiSigns in your Enterprise App](https://support.optisigns.com/hc/en-us/articles/4403616315539) for even more control over security options.

#### **How do I set up a Power BI service principal with OptiSigns?**

We have an entire article dedicated to this process! Please see:

* [Set Up a Power BI Service Principal for Use in OptiSigns](https://support.optisigns.com/hc/en-us/articles/32860569148819-How-to-Set-Up-a-PowerBI-Service-Principal-for-Use-in-OptiSigns)

Please note that the service principal option is only available to customers with an **Enterprise** plan.

#### **How can I edit the size of the screen on my display?**

To make sure your Power BI app displays properly, go to **View** within the Power BI application you want to display. Then hit **Fit to Page**.

![power bi fit to page](https://support.optisigns.com/hc/article_attachments/37192704471315)

Certain display devices may have additional requirements for displaying the report at the proper resolution. For example, mobile devices display at a different resolution than typical HD devices, and so some display issues may arise when setting reports to display on a mobile device.

In addition, certain hardware is not optimized for displaying Power BI. In these cases, we recommend our [OptiSigns Android Player](https://www.optisigns.com/product/hardware/android-player), which guarantees the best support for our software and Power BI in particular.

If issues persist, we recommend contacting our support team at [support@optisigns.com](mailto:support@optisigns.com).

#### **I'm having trouble displaying my Power BI report off MS Fabric.**

If you have a Power BI report created off MS Fabric, you'll need to make a slight tweak to the URL to get it to display using OptiSigns.

If created on Fabric, your Power BI URL should begin: **app.fabric.microsoft.com**

Simply change this to: **app.powerbi.com** while keeping all other parameters the same. This should fix any display issues.

#### **My Power BI report displays on my portal, but won't display on my screen. Help?**

This issue is usually caused by network connectivity issues at the device. We recommend checking and validating your device/screen's network connection.

If you have a Samsung SSSP or LG WebOS TV, there might be a different issue. Microsoft requires a minimum Chromium version of 95 for their apps to display. These TVs typically don't update very often. This is a Microsoft issue, and there is little we can do on our end.

If you have one of these TVs and wish to display SharePoint, we recommend our [Android Player](https://www.optisigns.com/product/hardware/android-player).

If you're still having issues, feel free to contact our support team at [support@optisigns.com](mailto:support@optisigns.com).

#### **My Power BI report lags and crashes frequently. Why?**

Lagging and crashing Power BI reports usually have to do with two factors:

* The device being used to run the OptiSigns app and display the report
* The size of the report

Simply put, the larger the size of the report, the more powerful device you'll need to display it without issue. Small reports can use weaker hardware, while large and sprawling reports will need more powerful or dedicated hardware.

This means, if you're having this issue, you'll need to either:

1. Reduce the size of the report you want to display
2. Improve the hardware you're using

We recommend using an [**OptiSigns Pro Player**](https://www.optisigns.com/product/hardware/pro-digital-signage-player)or [**OptiSigns ProMax Player**](https://www.optisigns.com/product/hardware/promax-digital-signage-player)for displaying large, heavy Power BI reports.

#### **Power BI Display for US Government Customers**

If you are a US government entity (federal, state, or local), you may be using Power BI for government. If so, your Power BI reports will use one of these URLs:

* **GCC**: `https://app.powerbigov.us`
* **GCC High**: [`https://app.high.powerbigov.us`](https://app.high.powerbigov.us)

If that is the case, your display won't work with the Power BI app. However, it is possible to create your Power BI as a Sharepoint application, then display it with our [**SharePoint app**](https://support.optisigns.com/hc/en-us/articles/4414539282067-Displaying-SharePoint-Sites-on-OptiSigns)**.**



---
Article URL: https://support.optisigns.com/hc/en-us/articles/360024859713-How-to-Display-Microsoft-Power-BI-Dashboards-Reports-with-OptiSigns