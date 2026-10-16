---
title: "Connectrix in CloudIQ!"
pubDate: 2019-04-30
postedAt: "09:58 AM"
description: "Background Just about 2 years ago I got my first look at CloudIQ and was immediately impressed. I mean, who wouldn’t be impressed by a Cloud Native Application that enables our customers to view the Health, Configuration, Capacity and Performance information of their entire inventory of Unity, VMAX, SC, and..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2019/04/connectrix-in-cloudiq.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250917034322/https://brasstacksblog.typepad.com/brass-tacks/2019/04/connectrix-in-cloudiq.html"
pdf: "/brasstacks/connectrix-in-cloudiq/connectrix-in-cloudiq.pdf"
comments:
  - author: "Pavel Karnaukh"
    date: "05/20/2019 at 03:28 PM"
    html: |-
      <p>Excellent overview! What about CloudIQ for Vmware?</p>
  - author: "Caminade"
    date: "05/29/2019 at 11:50 AM"
    html: |-
      <p>Hello<br />
      Very intersting but what are the ports used by CloudIQ collector to communciate with ESRS and with the switches ?</p>
---

<h1>Background</h1>
<p>Just about 2 years ago I got my first look at CloudIQ and was immediately impressed.&#0160;</p>
<p>I mean, who wouldn’t be impressed by a Cloud Native Application that enables our customers to view the Health, Configuration, Capacity and Performance information of their entire inventory of Unity, VMAX, SC, and XtremIO systems from a single pane of glass?</p>
<p>As I explored the early CloudIQ user interface, I remember thinking how amazing it would be if we could view SAN and host information from this interface as well.&#0160; I believed this type of ”end-to-end” information would make it much easier to troubleshoot and remediate things like the <a href="/brasstacks/slow-drains-are-impacting-your-san/">slow drain</a> and <a href="/brasstacks/slow-drain-due-to-bandwidth-mismatch-and-large-block-reads/">congestion spreading</a> events that have been experienced by many of our customers.&#0160;</p>
<p>Little did I know, less than a year later my team would be given the opportunity to add support for Connectrix products into CloudIQ and help make this end-to-end view of infrastructure a reality.</p>
<p>In this post I’ll provide a very high level overview of the data collection process used to support the Connectrix products as well as a couple of the important features that I believe you will find very useful when Connectrix in CloudIQ becomes available at the end of May.</p>
<h1>Connectrix in CloudIQ overview</h1>
<p>Rather than immediately dive into the different features and views, I’d like to start with overview of the process that we use to collect data.</p>
<p><a class="asset-img-link" href="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a4821607200d.jpg" style="display: inline;"><img alt="Overview" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0240a4821607200d image-full img-responsive" src="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a4821607200d.jpg" title="Overview" /></a><br />&#0160;</p>
<p>Starting from the bottom of the diagram, you’ll note that we plan to support both B-Series and MDS Series Connectrix products.&#0160; I should point out, that we can collect data from any FC switch running FOS 8.2.1a or above or NX-OS 8.3(2) and above (including non-Connectrix models).&#0160; However, in order for the switches to be visible in CloudIQ, the product will need to be under an active service contract with Dell EMC.&#0160; We validate the contract status using the product serial number.</p>
<p>The actual data collection process is periodically performed by the CloudIQ Collector (~once every 5 minutes).&#0160; Each time a collection is performed, the CloudIQ Collector will gather the required health, configuration, capacity and performance data from every switch in the environment via their REST API.&#0160; This information is then pushed back to Dell EMC via Secure Remote Services (SRS) and then makes its way to our CloudIQ backend where is it processed and securely stored.&#0160;</p>
<p>The CloudIQ Collector itself is fairly lightweight (&lt;700MB of disk space is required) and is based on Dell EMC Storage Resource Manager (SRM).&#0160; The collector also has the ability to collect VM information from vCenter.</p>
<p>One final point to note, the switches also have the capability to send alert information directly to our services organization (i.e., call home) and this capability does not require the CloudIQ collector, only SRS.&#0160;</p>
<h1>Important features</h1>
<p>When we first started this project, we wanted to make sure that the information we provided was always accurate, relevant and actionable.&#0160; To this end, we solicited a lot of input not only from our Customers, but also from our services team (since they are troubleshooting SAN issues all day) and have a really healthy understanding of what’s relevant when there’s a problem.&#0160; Because of this input, you’ll notice a number of features in our first release that are intended to help you troubleshoot in a more efficient manner.&#0160;</p>
<p>I’ll review a couple of those features next.</p>
<h2>Inventory of all Connectrix products including a product specific Health Score</h2>
<p>Once you&#39;ve started collecting data from your Connectrix products and logged into CloudIQ, you can immediately get a sense of the health of your Connectrix products by selecting “Inventory” from the navigation tree on the left side of the CloudIQ UI and then clicking on the “SAN” tab.&#0160; As shown below, each SAN system (switch) will be displayed as a tile that includes the health score associated with that product.</p>
<p><a class="asset-img-link" href="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a458d958200c.jpg"></a> <a class="asset-img-link" href="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a458d961200c.jpg"></a> <a class="asset-img-link" href="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a458d970200c.jpg"><img alt="Inventory" class="asset  asset-image at-xid-6a013487ed263f970c0240a458d970200c img-responsive" src="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a458d970200c.jpg" style="display: block; margin-left: auto; margin-right: auto;" title="Inventory" /></a>Starting from the top, each tile includes:</p>
<ul>
<li>A health score that represents the HW status of the switch. In the short term, you can expect the health score calculation to include whether or not the switch is experiencing congestion.&#0160;</li>
<li>The name of the product (e.g., Production SAN Extension). This is the user-friendly name you assigned to the product in your environment.</li>
<li>The model (e.g., Connectrix ED-DCX6-4B) and serial number (e.g., EAF300M001).</li>
<li>The Firmware Version (e.g, v8.2.1a)</li>
<li>Last Contact Time – The last time this product sent information back to CloudIQ.</li>
<li>As well as the Location and Site ID where the product was physically installed.</li>
</ul>
<p>Note: There is also a list view available that provides the same type of information but in a table format.</p>
<p>If you want more detailed configuration information about the switch, you can always click on its name and you’ll be brought to a detailed configuration view as shown below.</p>
<p><a class="asset-img-link" href="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a4a6af87200b.jpg"><img alt="DetaileConfig" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0240a4a6af87200b image-full img-responsive" src="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a4a6af87200b.jpg" style="display: block; margin-left: auto; margin-right: auto;" title="DetaileConfig" /></a></p>
<p>You’ll notice that this screen consists of:</p>
<ul>
<li>A Summary Header that provides much of the same information as the previous view did as well as the Switch uptime, Management IP Address and the WWNs associated with the product.</li>
<li>Five tabs that each provide detailed information about the Fabrics, Partitions (VFs or VSANs), Zones, Attached Devices and Components (e.g, FRUs) for this switch.</li>
</ul>
<p>Finally, if you want even more detailed information about your switch or you want to perform active management of a product (e.g., add a zone), you can click on the launch Element Manager link at the top right of the screen.&#0160; This will launch a browser pointed to the IP Address of the management interface of the product.&#0160; Here you can access the native switch management tool and do whatever you need.&#0160; BTW, I LOVE THIS FEATURE!&#0160; It’s so simple, yet so convenient.</p>
<h2>Capacity</h2>
<p>If you’re looking for port level information about your products, start from the left-hand navigation tree and select Capacity -&gt; System Capacity and then click the SAN tab.&#0160; For each product you’re managing in CloudIQ, you’ll see a tile similar to what is being shown below:</p>
<p><a class="asset-img-link" href="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a4a6af93200b.jpg"><img alt="SummaryCapacity" class="asset  asset-image at-xid-6a013487ed263f970c0240a4a6af93200b img-responsive" src="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a4a6af93200b.jpg" style="display: block; margin-left: auto; margin-right: auto;" title="SummaryCapacity" /></a></p>
<p>The donut graph gives a visual representation of the number of ports on the switch as well as the number of ports that have been consumed (e.g., are online) or are in need of attention (e.g., in an Error state).</p>
<p>If you’d like additional detail, click on the switch name and the Detailed Capacity view will be displayed as shown below.</p>
<p><a class="asset-img-link" href="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a482164c200d.jpg"><img alt="DetailedCapacity" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0240a482164c200d image-full img-responsive" src="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a482164c200d.jpg" style="display: block; margin-left: auto; margin-right: auto;" title="DetailedCapacity" /></a></p>
<p>The upper left side of the user interface provides the same information as the previous “System Capacity” view did.&#0160; However, depending on what type of interface you have selected (i.e., Online), the other views to the right as well as the table below the donut graph will be filtered accordingly.&#0160; This filtering can be combined so that you can limit what is displayed in the table view (at the bottom) to show only Online, F_Ports, that have registered as a storage port (for example).</p>
<h2>Performance</h2>
<p>If you’re looking for performance information about your products, start from the left-hand navigation tree and select Performance -&gt; System Performance and then click the SAN tab.&#0160; For each product you’re managing in CloudIQ, you’ll see a tile similar to what is being shown below:</p>
<p><a class="asset-img-link" href="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a4821650200d.jpg"><img alt="SummaryPerformace" class="asset  asset-image at-xid-6a013487ed263f970c0240a4821650200d img-responsive" src="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a4821650200d.jpg" style="display: block; margin-left: auto; margin-right: auto;" title="SummaryPerformace" /></a></p>
<p>This view contains:</p>
<ul>
<li>System Bandwidth – This represents the average amount of data being transmitted by the switch over the past 24 hours. You’ll also note the graph at the bottom of the dialog provides a historical view of the amount being transmitted during each sample interval.&#0160; Note, we’ve already been asked to update this to include a metric that represents what percentage of total system bandwidth is being consumed and we plan to do this in an upcoming relase.</li>
<li>Utilization &gt;= 80% - Number of switch interfaces that were running at greater than or equal to 80% utilization when the last collection was taken from the switch.</li>
<li>Congested - Number of switch interfaces that were congested (had a congestion ratio greater than or equal to 0.2) when the last collection was taken from the switch. NOTE: This is a REALLY COOL FEATURE.&#0160; If you don’t know how to calculate the congestion ratio or why it’s important, see our recent white paper on <a href="https://www.dellemc.com/resources/en-us/asset/white-papers/products/networking/h17762-connectrix-congestion-spreading-and-how-to-avoid-it-wp.pdf">Congestion Spreading and how to avoid it</a>.</li>
<li>Errors - Number of switch interfaces that met one of the following criteria when the last collection was taken from the switch:
<ul>
<li>A change in an interface error counter of greater than or equal to 100 occurred between the current sample and a previous sample.</li>
<li>Greater than or equal to 50% of the samples from a given interface over the past hour have incremented an error counter.</li>
<li>Greater than or equal to 50% of the hour intervals from a given interface over the past 24 hours have met either of the above criteria.</li>
</ul>
</li>
</ul>
<ul>
<li>Link Resets – Similar to Errors (above) but with specific criteria related to the reception of Link Reset primitives.</li>
</ul>
<p>After looking through all of this information, you’d like to see more detailed performance information, you can click on the switch name and a number of graphs showing detailed performance information will be displayed.&#0160; One of these graphs related to congestion is shown below.</p>
<p><a class="asset-img-link" href="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a4821663200d.jpg"><img alt="Perfdetails" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0240a4821663200d image-full img-responsive" src="/brasstacks/connectrix-in-cloudiq/6a013487ed263f970c0240a4821663200d.jpg" style="display: block; margin-left: auto; margin-right: auto;" title="Perfdetails" /></a></p>
<p>Currently, this graph displays a number of data points each representing the sum of “time spent at zero transmit credit” across all interfaces during each sampling interval.&#0160; This can be useful when trying to understand if you’ve had a SAN event that could have impacted overall performance.</p>
<h2>What’s next?</h2>
<p>While we believe we’ve been able to provide some useful functionality, we also know that there’s a lot more we could do going forward.&#0160; I expect we’ll be working in three areas:</p>
<ol>
<li>Customer originated enhancement requests. We built this tool with our end users in mind, so if you think we’re missing something or have a great idea for a feature, let us know!&#0160;</li>
<li>Predictive Analytics related to optic health. Shortly after we GA, we will start looking into how to predict optic failure based on TX and RX optical power, bit errors and other link events.</li>
<li>More granular performance information. We would like to make it possible for you to zoom into a chart (e.g., the Congestion chart above) and allow you to easily view the top contributors.&#0160;</li>
</ol>
<p>All that said, we’re just super excited to reach this milestone and we look forward to helping you get the most from your SAN.</p>
<p>Let us know how we can help!</p>
<p>Thanks for reading!</p>
<p>&#0160;</p>
