---
title: "Let’s play in an AWS based SANdbox – Part 2 Setting up your AWS VPC and networks"
pubDate: 2022-09-30
postedAt: "04:42 PM"
description: "In my previous post, I introduced the SANdbox Github repo and described the work that had been done to create an Virtual Lab that is capable of supporting NVMe/TCP traffic. In this post I’ll walk you through the steps to create your own SANdbox VPC in AWS that will eventually..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2022/09/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250912222026/https://brasstacksblog.typepad.com/brass-tacks/2022/09/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks.html"
pdf: "/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks.pdf"
comments: []
---

<p>In my previous post, I introduced the SANdbox Github repo and described the work that had been done to create an Virtual Lab that is capable of supporting NVMe/TCP traffic.</p>
<p>In this post I’ll walk you through the steps to create your own SANdbox VPC in AWS that will eventually look similar to the following.</p>
<p><a class="asset-img-link" href="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a308e1f3d5200c.png" style="display: inline;"><img alt="AWSConfig" border="0" class="asset  asset-image at-xid-6a013487ed263f970c02a308e1f3d5200c image-full img-responsive" src="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a308e1f3d5200c.png" title="AWSConfig" /></a></p>
<p>Before I get started, I need to acknowledge two sources of information that were invaluable to me as I was getting started with AWS:</p>
<ol>
<li>The AWS documentation – I found <a href="https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario2.html">an article</a> that seemed to describe exactly what I wanted to do but I didn’t have enough context/knowledge of AWS at the time to be able to follow it successfully.</li>
<li>This “<a href="https://www.youtube.com/watch?reload=9&amp;v=uo_Xf_pGTvg">HOW TO Build a Home Lab in AWS for FREE</a>” video by Jon Good. It was incredibly helpful and I highly recommend reviewing it before continuing with the following steps.</li>
</ol>
<h2>Create a Free AWS account</h2>
<ol>
<li>Click <a href="https://aws.amazon.com/free/">here</a> to create a Free AWS account.</li>
<li>Provide an email address</li>
<li>Provide an AWS account name</li>
<li>Verify the email Address you provided by taking note of the Verification code they provide you an then entering it into the browser when prompted.</li>
<li>Create your Root user password.</li>
<li>Provide your contact information</li>
<li>Provide credit card information</li>
<li>Confirm your identity (I chose to use SMS)</li>
<li>Select a support plan (I chose Basic support – Free)</li>
<li>Click <strong>Complete sign up</strong></li>
<li>Click <strong>Go to the AWS console</strong></li>
<li>Enter or ensure that the correct email address is provided and click <strong>Next</strong>.</li>
<li>Enter the password associated with the email address provided and click <strong>Next</strong>.</li>
</ol>
<h2>Secure your account with MFA</h2>
<ol>
<li>In AWS, under Console Home, click <strong>IAM</strong>
<ol>
<li>Note: If you ever lose track of a particular view or service, you can always click the Services icon at the top of the page or search for the service name you want to access and get to it that way. I do this all the time for accessing my “EC2” instances.</li>
</ol>
</li>
<li>In the IAM dashboard, click <strong>Add MFA</strong>.</li>
<li>Under Your Security Credentials &gt; Multi-factor authentication (MFA), click <strong>activate MFA</strong>.</li>
<li>Choose the type of MFA device to assign (I chose “Virtual MFA device”) and then click <strong>Continue</strong></li>
<li>In the “Set Up virtual MFA device” dialog, you will be prompted to:
<ol>
<li>Install a compatible app on your mobile device or computer (I chose the App “Authenticator” because it was supported on IOS and had good reviews online)</li>
<li>Use the virtual MFA app and your device’s camera to scan the QR code shown within AWS.</li>
<li>Enter two consecutive tokens from the Authenticator APP, then click <strong>OK, </strong>and you should see “You have successfully assigned a virtual MFA. Click <strong>Close</strong></li>
<li>Click on “Dashboard” (left side of the screen) and ensure there is a green check mark next to “Root user has MFA”.</li>
</ol>
</li>
<li>Click on the user name at the top right of the screen (e.g., <strong>SANdboxBlog</strong>) and then click <strong>Sign out</strong></li>
</ol>
<p><a class="asset-img-link" href="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a308e1f3ec200c.png" style="display: inline;"><img alt="IAM" border="0" class="asset  asset-image at-xid-6a013487ed263f970c02a308e1f3ec200c image-full img-responsive" src="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a308e1f3ec200c.png" title="IAM" /></a></p>
<h2>Setup a Billing Alert</h2>
<p>Note: Jon Good recommended this and I cannot stress how good of an idea it is.&#0160; You’d be surprised how quickly you can blow through $10 once you start using non-free instances and Elastic IP Addresses. My only regret is I did not also create a $100 alert :-) … do not make the same mistake I did!&#0160; The steps for doing this are very straight-forward and can be found <a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html">here</a>.</p>
<p>Here’s my alarm configuration after setup.</p>
<p><a class="asset-img-link" href="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a2eed7f847200d.png" style="display: inline;"><img alt="Alarms" border="0" class="asset  asset-image at-xid-6a013487ed263f970c02a2eed7f847200d image-full img-responsive" src="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a2eed7f847200d.png" title="Alarms" /></a></p>
<h2>Create a Virtual Private Cloud (VPC)</h2>
<p>The VPC is the top level “container” into which all of your Virtual Resources will be deployed.&#0160;</p>
<ol>
<li>To create a VPC, click on <strong>Services</strong> (at the top left of AWS console screen) and click on (or search for) <strong>VPC</strong>. Click <strong>Create VPC</strong>.</li>
<li>Under VPC settings, I chose <strong>VPC and more.</strong></li>
<li>Under Name tag auto-generation, I provided a tag of <strong>SANdboxBlog</strong>.</li>
<li>I decided to use a <strong>single Availability Zone</strong> as my lab configuration does not require HA.</li>
<li>I increased the number of private subnets from 1 to 2.</li>
<li>All other settings were left at defaults.</li>
<li>The VPC preview should look similar to the following</li>
<li>Click <strong>Create VPC</strong> and the VPC workflow will run. Click View VPC after the workflow completes.</li>
</ol>
<p><a class="asset-img-link" href="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a2eed7f84f200d.png" style="display: inline;"><img alt="VPC Preview" border="0" class="asset  asset-image at-xid-6a013487ed263f970c02a2eed7f84f200d image-full img-responsive" src="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a2eed7f84f200d.png" title="VPC Preview" /></a></p>
<h2>Create and associate Security Groups</h2>
<p>Creating and managing security groups is a tedious but necessary task.&#0160; It allows you to define the sources (e.g., IP Addresses) that can be used to access the resources inside of your VPC.&#0160; I created three Security Groups, one for my LAN (public facing) network and two for my SANs (e.g., SAN A and SAN B). I’ve summarized the SGs I created below for ease of reference.</p>
<h3>LAN-Public</h3>
<table>
<tbody>
<tr>
<td width="89">
<p>Name</p>
</td>
<td width="49">
<p>IP ver</p>
</td>
<td width="108">
<p>Type</p>
</td>
<td width="72">
<p>Protocol</p>
</td>
<td width="84">
<p>Port Range</p>
</td>
<td width="138">
<p>Source</p>
</td>
</tr>
<tr>
<td width="89">
<p>SSH</p>
</td>
<td width="49">
<p>IPv4</p>
</td>
<td width="108">
<p>SSH</p>
</td>
<td width="72">
<p>TCP</p>
</td>
<td width="84">
<p>22</p>
</td>
<td width="138">
<p>0.0.0.0/0</p>
</td>
</tr>
<tr>
<td width="89">
<p>HTTPS</p>
</td>
<td width="49">
<p>IPv4</p>
</td>
<td width="108">
<p>HTTPS</p>
</td>
<td width="72">
<p>TCP</p>
</td>
<td width="84">
<p>443</p>
</td>
<td width="138">
<p>0.0.0.0/0</p>
</td>
</tr>
</tbody>
</table>
<h3>SAN A and SAN B</h3>
<table>
<tbody>
<tr>
<td width="89">
<p>Name</p>
</td>
<td width="49">
<p>IP ver</p>
</td>
<td width="108">
<p>Type</p>
</td>
<td width="72">
<p>Protocol</p>
</td>
<td width="84">
<p>Port Range</p>
</td>
<td width="138">
<p>Source</p>
</td>
</tr>
<tr>
<td width="89">
<p>mDNS</p>
</td>
<td width="49">
<p>-</p>
</td>
<td width="108">
<p>Custom UDP</p>
</td>
<td width="72">
<p>UDP</p>
</td>
<td width="84">
<p>5353</p>
</td>
<td width="138">
<p>0.0.0.0/0</p>
</td>
</tr>
<tr>
<td width="89">
<p>NVMe/TCP Discovery</p>
</td>
<td width="49">
<p>IPv4</p>
</td>
<td width="108">
<p>Custom TCP</p>
</td>
<td width="72">
<p>TCP</p>
</td>
<td width="84">
<p>8009</p>
</td>
<td width="138">
<p>0.0.0.0/0</p>
</td>
</tr>
<tr>
<td width="89">
<p>NVMe/TCP IO</p>
</td>
<td width="49">
<p>IPv4</p>
</td>
<td width="108">
<p>Custom TCP</p>
</td>
<td width="72">
<p>TCP</p>
</td>
<td width="84">
<p>4420</p>
</td>
<td width="138">
<p>0.0.0.0/0</p>
</td>
</tr>
<tr>
<td width="89">
<p>PING</p>
</td>
<td width="49">
<p>-</p>
</td>
<td width="108">
<p>All ICMP – IPv4</p>
</td>
<td width="72">
<p>ICMP</p>
</td>
<td width="84">
<p>ALL</p>
</td>
<td width="138">
<p>0.0.0.0/0</p>
</td>
</tr>
</tbody>
</table>
<h2>Create the “LAN-Public” Security Group</h2>
<ol>
<li>From “Services”, click on <strong>EC2</strong>. (Not really required but I like to start from the EC2 dashboard for everything)</li>
<li>On the left side of the console scroll down to “Network &amp; Security” and click on <strong>Security Groups </strong>and then<strong> Create Security Group.</strong></li>
<li>Add a Security Group Name (e.g., LAN-Public)</li>
<li>Add a Description (e.g., Allows SSH and HTTP access to instances)</li>
<li><strong><span style="color: #bf00bf;">VERY IMPORTANT</span></strong> Ensure the correct VPC is selected. The default VPC listed in the VPC field is probably not what you want. Click on the ‘X’ in the right side of the VPC field and ensure you have selected the correct VPC. In my case I selected the SANdboxBlog-vpc. If you haven’t already done this, take note of the last four digits of your VPCs instance ID.&#0160; In my case it’s “a245”, you will use this later on. Also, I highly recommend creating a diagram of your environment to keep track of all of the instance IDs. A completed example diagram will be provided at the end of this post.&#0160;</li>
<li>Create Inbound rules – As described in the LAN-Public table above, we need to create rules that will allow for both SSH and HTTPS access to our instances.</li>
</ol>
<p><strong>&#0160;SSH</strong></p>
<ol>
<li>Under Inbound rules, click <strong>Add Rule</strong></li>
<li>From the Type pulldown, select <strong>SSH</strong>. This will automatically populate the Protocol and Port Range fields for you.</li>
<li>From the Source pulldown select Anywhere-IPv4. The IP address of 0.0.0.0/0 will automatically be added to your list of sources.</li>
</ol>
<p style="padding-left: 40px;">NOTE: Using Anywhere-IPv4 is NOT a best practice. Ideally, you would specify the IP Address of the system you will be using to access your VPC.</p>
<p><strong>HTTPS</strong></p>
<ol>
<li>Click <strong>Add Rule</strong></li>
<li>From the Type pulldown, select <strong>HTTPS</strong>. This will automatically populate the Protocol and Port Range fields for you.</li>
<li>From the Source pulldown select Anywhere-IPv4. The IP address of 0.0.0.0/0 will automatically be added to your list of sources.</li>
</ol>
<p>Confirm that your security group looks similar to what is shown below and then click <strong>Create Security Group</strong>.</p>
<p><a class="asset-img-link" href="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a30d4f4bf4200b.png" style="display: inline;"><img alt="LAN-Public SG" border="0" class="asset  asset-image at-xid-6a013487ed263f970c02a30d4f4bf4200b image-full img-responsive" src="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a30d4f4bf4200b.png" title="LAN-Public SG" /></a></p>
<p>Once the SG was created I took note of the Instance number for the LAN-Public Security Group (i.e., 4872) and added this to my topology diagram.</p>
<h2>Create the “SAN A” Security Group</h2>
<ol>
<li>On the left side of the console click on <strong>Security Groups </strong>and then<strong> Create Security Group.</strong></li>
<li>Add a Security Group Name (e.g., SAN A)</li>
<li>Add a Description (e.g., SAN A is a private network for NVMe/TCP Discovery and IO traffic.)</li>
<li>VERY IMPORTANT Ensure the correct VPC is selected. The default VPC listed in the VPC field is probably not what you want. In my case I selected the SANdboxBlog-vpc and it has an instance ID of “a245”.&#0160;</li>
<li>Create Inbound rules – As described in the SAN A and SAN B table above, we need to create rules that will allow for mDNS, NVMe/TCP Discovery, NVMe/TCP IO and Ping to be used between the instances in our VPC.</li>
</ol>
<p><strong>&#0160;mDNS</strong></p>
<ol>
<li>Under Inbound rules, click <strong>Add Rule</strong></li>
<li>From the Type pulldown, select <strong>Custom UDP</strong>. This will automatically populate the Protocol field for you.</li>
<li>In the Port range field enter <strong>5353</strong></li>
<li>From the Source pulldown select <strong>Anywhere-IPv4</strong>. The IP address of 0.0.0.0/0 will automatically be added to your list of sources.</li>
<li>Provide a description (e.g., <strong>mDNS</strong>)</li>
</ol>
<p><strong>NVMe/TCP Discovery</strong></p>
<ol>
<li>Click <strong>Add Rule</strong></li>
<li>From the Type pulldown, select <strong>Custom TCP</strong>. This will automatically populate the Protocol field for you.</li>
<li>In the Port range field enter <strong>8009</strong></li>
<li>From the Source pulldown select <strong>Anywhere-IPv4</strong>. The IP address of 0.0.0.0/0 will automatically be added to your list of sources.</li>
<li>Provide a description (e.g., <strong>NVMe/TCP Discovery</strong>)</li>
</ol>
<p><strong>NVMe/TCP IO</strong></p>
<ol>
<li>Click <strong>Add Rule</strong></li>
<li>From the Type pulldown, select <strong>Custom TCP</strong>. This will automatically populate the Protocol field for you.</li>
<li>In the Port range field enter <strong>4420</strong></li>
<li>From the Source pulldown select <strong>Anywhere-IPv4</strong>. The IP address of 0.0.0.0/0 will automatically be added to your list of sources.</li>
<li>Provide a description (e.g., <strong>NVMe/TCP IO</strong>)</li>
</ol>
<p><strong>PING</strong> (this is not technically necessary, but you will thank me later).</p>
<ol>
<li>Click <strong>Add Rule</strong></li>
<li>From the Type pulldown, select <strong>All ICMP – IPv4</strong>. This will automatically populate the Protocol and Port range fields for you.</li>
<li>From the Source pulldown select <strong>Anywhere-IPv4</strong>. The IP address of 0.0.0.0/0 will automatically be added to your list of sources.</li>
<li>Provide a description (e.g., <strong>PING</strong>)</li>
</ol>
<p>Confirm that your security group looks similar to what is shown below and then click <strong>Create Security Group</strong>.</p>
<p><a class="asset-img-link" href="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a30d4f4c00200b.png" style="display: inline;"><img alt="SAN SG" border="0" class="asset  asset-image at-xid-6a013487ed263f970c02a30d4f4c00200b image-full img-responsive" src="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a30d4f4c00200b.png" title="SAN SG" /></a></p>
<h2>Create the “SAN B” Security Group</h2>
<p>Using the information from the SAN A and SAN B table above, repeat the steps outlined in “Create the SAN A Security Group” and create another Security Group for SAN B.</p>
<p>OR... You can save a ton of time and do the following</p>
<ol>
<li>Under <strong>Actions</strong>, at the top of the “SAN A Security Group” configuration screen, you can chose “Copy to a new security group”.</li>
</ol>
<p><strong><span style="color: #bf00bf;">VERY IMPORTANT</span></strong> After providing a “Security group name” (e.g., SAN B) and a Description, you will still need to ensure the correct VPC is selected. The default VPC listed in the VPC field is probably not what you want.&#0160; In my case I selected the SANdboxBlog-vpc and it has an instance ID of “a245”.</p>
<ol start="2">
<li>Click <strong>Create Security Group</strong></li>
</ol>
<h2>Create your first EC2 Instances</h2>
<p>Amazon Elastic Compute Cloud (EC2) instances can be thought of as virtual servers.&#0160; For the purposes of the SANdbox configuration, I’ve chosen to use EC2 instances that are running Ubuntu 20.04.&#0160; When I was first getting started and needed to work my way through the process of setting up the environment and familiarizing myself with AWS in general, I chose EC2 instances that were available in the free tier. This means there is no charge up to a certain amount of usage.&#0160; I will walk you through doing the same for two instances and will get us to the point where you can connect to each instance with SSH and ping across the network interfaces used for SAN A.&#0160; We will not be setting up SAN B right now, just validating connectivity across one SAN is enough (for now).&#0160;</p>
<ol>
<li>From the “EC2 Dashboard”, click <strong>Launch Instance</strong></li>
<li>Provide a “Name” for the instance (e.g., Host1)</li>
<li>Under “Application and OS Images (Amazon Machine Image)”, click on ubuntu and then select a particular version. I chose “Ubuntu Server 20.04 LTS (HVM), SSD Volume Type” because it was “Free Tier Eligible”, when we actually create the instances we will use for NVMe/TCP testing, we will make different choices that will have a different cost profile. Leave Architecture set to <strong>64-bit (x86)</strong></li>
<li>Under “Instance type”, select <strong>micro</strong> again because it is Free tier eligible.</li>
<li>Under “key pair (login), select <strong>Create new key pair</strong>
<ol>
<li>In the Create key pair dialog, provide a Key Pair name, I chose to use <strong>SANdboxBlog</strong></li>
<li>Select a “Key pair type” of <strong>RSA</strong></li>
<li>Select a “Private key file format” of <strong>.ppk</strong></li>
<li>Click <strong>Create key pair</strong> and a file (e.g., SANdboxBlog.ppk) will be downloaded to your system. You will need this file when we connect to the instance via PuTTY in a subsequent step.</li>
<li>Ensure that your key name (e.g., SANdboxBlog) is shown in the <strong>Key pair name – required</strong></li>
</ol>
</li>
<li>Under “Network Settings” click on <strong>Edit</strong>
<ol>
<li>Under “VPC”, ensure the correct VPC is selected (e.g., SANdboxBlog-vpc)</li>
<li>Under “Subnet”, ensure your public network is selected (e.g., <strong>SANdboxBlog-subnet-public1-us-east-1a</strong>)</li>
<li>Under “Auto-assign public IP”, ensure it is set to <strong>Disable</strong></li>
<li>Under “Firewall (security groups)”, click on “<strong>Select existing security group</strong>”</li>
<li>Under “Common security groups”, leave it <strong>blank</strong></li>
<li>Click <strong>Advanced network configuration</strong></li>
<li>Under “Network Interface 1”
<ol>
<li>Set the “Description” to <strong>Public-LAN</strong></li>
<li>Under the “Security groups” pull down menu, choose <strong>LAN-Public</strong></li>
<li>Leave everything else at the default setting</li>
</ol>
</li>
<li>Click <strong>Add network interface</strong>
<ol>
<li>Set the “Description” to <strong>SAN A</strong></li>
<li>Under the “Subnet” pull down menu, select the <strong>SAN A subnet</strong></li>
<li>Under the “Security groups” pull down menu, choose <strong>SAN A</strong></li>
<li>Leave everything else at the default setting</li>
</ol>
</li>
<li>Note, this instance type only supports two network interfaces, so we will only configure SAN A for now.</li>
</ol>
</li>
</ol>
<ol start="7">
<li>Under the Summary tab (on the right side of the console)
<ol>
<li>For Number of instances, specify 2</li>
<li>Then click <strong>Launch instance</strong></li>
<li>Click <strong>View all instances </strong>when the button becomes available.</li>
</ol>
</li>
</ol>
<h2>Take an inventory of your Virtual Infrastructure</h2>
<ol>
<li>Now that your EC2 instances are up, ensure that you name them appropriately, I chose <strong>Host 1</strong> and <strong>Host 2</strong>. You can rename them in the EC2 Dashboard by clicking in the <strong>Name</strong> field.</li>
<li>For each Host, take note of at least the last four digits of the instance ID.</li>
<li>For each Host, click on the <strong>Instance ID </strong>and select the <strong>Networking</strong> tab</li>
<li>Scroll down to the Network Interfaces section and take note of the last four digits of each Interface ID (you may need to expand the Interface ID column to see the last four digits). You’ll also want to understand what network each interface is associated with, and the Description field should answer this question for you.</li>
<li>You’ll also want to take note of the IPv4 addresses for the SAN A interfaces. We will be using them to verify connectivity in the final step.</li>
<li>I highly recommend keeping track these instance and interface IDs because we will use them later. Here’s what my configuration looks like at this point.&#0160; Note that the IP address for the LAN-Public interfaces are Elastic 1 and Elastic 2, we will actually assign them next.</li>
</ol>
<p><a class="asset-img-link" href="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a30d4f4c30200b.png" style="display: inline;"><img alt="Inventory1" border="0" class="asset  asset-image at-xid-6a013487ed263f970c02a30d4f4c30200b image-full img-responsive" src="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a30d4f4c30200b.png" title="Inventory1" /></a></p>
<h2>Create and Assign Elastic IPs</h2>
<p>If I was only using a single network interface per instance, I could have had a public IP Address assigned to each Interface.&#0160; However, because this functionality is not supported when you have more than one network interface on an instance, I’ve found the easiest way to get access to my instances is to use Elastic IPs.&#0160; Unfortunately, Elastic IPs are not free, so please be advised.</p>
<ol>
<li>Under “Network &amp; Security” select <strong>Elastic IPs </strong>and then click on <strong>Allocate Elastic IP address</strong></li>
<li>Click Allocate and you will be returned to the Elastic IP Address screen. Take note of the Allocated IPv4 address.&#0160; In my case it is 3.230.foo.bar</li>
<li>Select the IP Address (little check box to the left of the IP), click <strong>Actions</strong> and then <strong>Associate Elastic IP address</strong></li>
<li>Under resource type, choose <strong>Network interface</strong> and then click inside of the Network Interface box and select the Public-LAN interface of Host 1. BTW, you need to use the resource ID of the interface and this is why it is so important to keep an updated diagram of your virtual infrastructure as you create it.&#0160; In my case the last four digits of the interface on Host 1 that is connected to Public-LAN is 20d1.&#0160; Clicked on the correct interface ID and then click <strong>Associate</strong>.</li>
<li>Because you need two Elastic IP addresses, click on <strong>Allocate Elastic IP address </strong>a second time and repeat the above steps for the Public-LAN interface on Host 2. My second Elastic IP was 34.234.you.too</li>
</ol>
<h2>Connect to your Instances</h2>
<p>To complete this next step you’re going to need the SANdboxBlog.ppk file that was downloaded to your system when you were creating your instances.&#0160; You’re also going to need PuTTY installed on your system as well.&#0160;</p>
<ol>
<li>Open PuTTY</li>
<li>In the <strong>Host Name (or IP Address)</strong> field enter the Elastic IP Address associated with Host 1 (e.g., 3.230.foo.bar)</li>
<li>Under connection -&gt; Data enter the default user name for ubuntu in AWS (<strong>ubuntu</strong>)</li>
<li>Under connection -&gt; SSH -&gt; Auth, browse to the location of the SANdboxBlog.ppk file.</li>
<li>Click Open</li>
<li>Accept the warning about the Host Key</li>
<li>And you should be logged into your Host 1 instance.</li>
<li>Ping the IP Address of the SAN A interface on Host 2, in my case, this IP Address is 10.0.134.136 and verify that it was successful</li>
</ol>
<p><a class="asset-img-link" href="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a2eed7f8d3200d.png" style="display: inline;"><img alt="PING" border="0" class="asset  asset-image at-xid-6a013487ed263f970c02a2eed7f8d3200d image-full img-responsive" src="/brasstacks/lets-play-in-an-aws-based-sandbox-part-2-setting-up-your-aws-vpc-and-networks/6a013487ed263f970c02a2eed7f8d3200d.png" title="PING" /></a></p>
<h2>Next steps</h2>
<p>So far we’ve created a Free AWS account, configured MFA, setup billing alerts, created a VPC with three networks, created 3 security groups and verified basic connectivity to and within our VPC using a pair of free tier servers.&#0160;</p>
<p>Next time we’re going to deploy 3 larger EC2 instances, and install:</p>
<ol>
<li>nvme-stas on our Host EC2 instance,</li>
<li>SmartFabric Storage Software on our Centralized Discovery Controller (CDC) EC2 instance, and</li>
<li>SPDK on our Storge EC2 instance.</li>
</ol>
<p>Thanks for reading!</p>
