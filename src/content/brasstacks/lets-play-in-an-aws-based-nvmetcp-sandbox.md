---
title: "Let’s play in an AWS based NVMe/TCP SANdbox!"
pubDate: 2022-09-23
postedAt: "08:25 AM"
description: "One of the great things about NVMe/TCP is its flexibility. Not only can you use the NVMe/TCP protocol to connect hosts to storage systems over an arbitrary IP network topology; as originally described here, you can also run it in a surprising number of operating environments, including: traditional enterprise environments..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2022/09/lets-play-in-an-aws-based-nvmetcp-sandbox.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250910105353/https://brasstacksblog.typepad.com/brass-tacks/2022/09/lets-play-in-an-aws-based-nvmetcp-sandbox.html"
pdf: "/brasstacks/lets-play-in-an-aws-based-nvmetcp-sandbox/lets-play-in-an-aws-based-nvmetcp-sandbox.pdf"
comments: []
---

<p>One of the great things about NVMe/TCP is its flexibility.</p>
<p>Not only can you use the NVMe/TCP protocol to connect hosts to storage systems over an arbitrary IP network topology; as originally described <a href="https://www.dell.com/en-us/blog/the-future-of-software-defined-networking-for-storage-connectivity/">here,</a> you can also run it in a surprising number of operating environments, including:</p>
<ul>
<li>traditional enterprise environments that utilize array-based storage solutions (e.g., PowerStore and PowerMax),</li>
<li>next generation operating environments that utilize Software Defined Storage (e.g., PowerFlex),</li>
<li>completely new use cases, such allowing applications running on the Edge to access centralized block storage resources, and most recently,</li>
<li>deploying your NVMe/TCP solution in the Cloud (e.g., AWS) and using the resulting &quot;Virtual Lab&quot; to simply get familiar with an NVMe IP-Based SAN, or more importantly test and validate your infrastructure automation software before you use it in production.</li>
</ul>
<p>The last item, especially the part about using AWS as a Virtual Lab, needs a bit more explanation.&#0160; Along these lines, this blog post series will:</p>
<ol>
<li>Provide an overview of the automation tools being made available in the SANdbox Github repository,</li>
<li>Provide the step-by-step instructions required to configure a AWS based NVMe/TCP test environment, and then</li>
<li>Demonstrate how you can get started with automating your storage provisioning tasks by using the PowerShell, Python or Ansible scripts that we will provide in SANdbox.</li>
</ol>
<h1>Introducing SANdbox!</h1>
<p><a href="https://github.com/dell/SANdbox">SANdbox</a> is a Github repo that provides access to the resources you will need when automating your NVMe IP-Based SAN. This includes:</p>
<h2>Documentation</h2>
<p><a href="https://github.com/dell/SANdbox/tree/main/Documentation">Start here</a> if you’re just coming up to speed on the concept of an NVMe IP-Based SAN.&#0160; You’ll find links to an IP-Based SAN introductory level blog post as well as links to two detailed SNIA presentations describing how Discovery Automation works at a protocol level.&#0160;</p>
<p>There’s also a link to Dell’s SmartFabric Storage Software (SFSS) deployment guide. It covers not only how to install SFSS, but also the basic network topologies that are currently supported as well as step by step configuration examples.</p>
<h2>Centralized Discovery Controller (CDC) <a href="https://github.com/dell/SANdbox/tree/main/Centralized%20Discovery%20Controller%20(CDC)">Downloads</a></h2>
<p>If you’ve been following the NVMe IP-Based SAN space for a little while, you probably already know that a group of companies identified a scalability problem related to the management of IP-Based SANs and decided to work together to solve it.&#0160; The result of this work can be found in a couple of NVM Express Technical Proposals (i.e., TP8009 and TP8010).&#0160;</p>
<ul>
<li>TP8009 describes how hosts can automatically discover subsystems using mDNS or DNS.</li>
<li>TP8010 defines the concept of a Centralized Discovery Controller (CDC) that limits the number of storage subsystem interfaces visible to each host. As most people who have dealt with FC SANs can attest, this functionality is very important as environments scale up.</li>
</ul>
<p>To help potential IP-Based SAN users get familiar with the usage of a CDC, Dell has made our implementation of a CDC, “SmartFabric Storage Software (SFSS)” available for download for trial purposes. Please note, this version is for trial and test purposes only and no support is available. If you want the latest, fully featured and fully supported version of SFSS, you need to purchase a license.</p>
<p>If you don’t want to download and install SFSS, either on your own infrastructure or on AWS, you can always give our <a href="https://www.dell.com/en-us/dt/product-demos/smartfabric-storage-software/index.htm?ref=DemoCenter">Interactive Demo</a> a try.&#0160; &#0160;&#0160;&#0160;</p>
<h2>Toolkit</h2>
<p>Once you’ve installed SFSS and understand the basics of interacting with it, you’ll probably be interested in learning how to automate the configuration steps and interact with your infrastructure programmatically. To this end, Dell has provided <a href="https://github.com/dell/SANdbox/tree/main/Toolkit">sample scripts</a> that will help you learn the basics.&#0160; Currently we’re providing PowerShell and Python examples and will be adding Ansible soon.</p>
<p>Both the PowerShell and Python scripts will allow you to:</p>
<ol>
<li>connect to the SFSS via the REST API,</li>
<li>retrieve a copy of the name server database,</li>
<li>add all of the NS entries to a single zone, and then</li>
<li>activate the zoning configuration.</li>
</ol>
<p>The experienced SAN admins amongst you will immediately recognize that zoning all of the ports together is NOT something that would typically be done! However, the example will give you enough information to do something a bit more realistic, such as allowing hosts to access a subset of the available subsystem interfaces.</p>
<h2>Virtual Lab</h2>
<p>If you’re interested in experimenting with an NVMe IP-Based SAN but you don’t have the HW infrastructure to do so, you can run all of it in AWS and experiment with it there on your own! The configuration I’m experimenting with is shown below.</p>
<p><a class="asset-img-link" href="/brasstacks/lets-play-in-an-aws-based-nvmetcp-sandbox/6a013487ed263f970c02a30d4e4238200b.png" style="display: inline;"><img alt="AWSConfig" border="0" class="asset  asset-image at-xid-6a013487ed263f970c02a30d4e4238200b image-full img-responsive" src="/brasstacks/lets-play-in-an-aws-based-nvmetcp-sandbox/6a013487ed263f970c02a30d4e4238200b.png" title="AWSConfig" /></a></p>
<p>In my AWS configuration I&#39;ve created:</p>
<ol>
<li>Three EC2 instances (Host 1, SFSS, Storage) all running Ubuntu 20.04
<ol>
<li>The <strong>Host</strong> instance utilizes the Dell maintained open source nvme discovery client “nvme-stas”</li>
<li>The <strong>SFSS</strong> instance is running our SFSS application and it handles all aspects of discovery automation</li>
<li>The <strong>Storage</strong> instance is running either nvmet or our “Dell End Point Simulator” that allows you to simulate pull and push registration from the command line. &#0160;</li>
</ol>
</li>
<li>A public facing network that I am using to access the instances from my desktop. This allows me to run my PowerShell or python scripts locally and configure my SFSS instance running in AWS.</li>
<li>Two private networks (i.e., SAN A and SAN B) that will allow you test the impact that things like zoning changes, or loss of connectivity to the CDC will have on your hosts ability to access block storage.</li>
</ol>
<p>The <a href="https://github.com/dell/SANdbox/tree/main/VirtualLab">Virtual Lab directory</a> will eventually contain all of the information and configuration steps you’ll need to setup an AWS based virtual lab of your own that is capable of using NVMe/TCP to connect from your host to your subsystem. Much more will be coming in this area.</p>
<p>Take a look at <a href="https://github.com/dell/SANdbox">SANdbox</a> today and take what you need or feel free to contribute!<br /><br />The next post in this series will provide the step-by-step instructions to setup your AWS based NVMe/TCP lab... Stay tuned.</p>
<p>#iworkfordell</p>
