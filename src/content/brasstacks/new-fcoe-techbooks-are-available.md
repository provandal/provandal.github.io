---
title: "New FCoE TechBooks are available!"
pubDate: 2012-02-27
postedAt: "10:52 AM"
description: "Over the past couple of months we’ve been working on adding some FCoE specific “Blade Server” information to the FCoE TechBook. Actually the vast majority of the work was done by two of my colleagues, Aditya Nadkarni and Shreedhan Nikam (more about them later). Early on in this process of..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2012/02/new-fcoe-techbooks-are-available.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250910174954/https://brasstacksblog.typepad.com/brass-tacks/2012/02/new-fcoe-techbooks-are-available.html"
pdf: "/brasstacks/new-fcoe-techbooks-are-available/new-fcoe-techbooks-are-available.pdf"
comments:
  - author: "Alberto"
    date: "02/27/2012 at 03:05 PM"
    html: |-
      <p>Hi Erik, thanks for linking these documents, they&#39;re really interesting.</p>
      <p>I was reading through the Nexus information on the case studies and I think it&#39;ll be worth it to include the Cisco B22 FEX for HP&#39;s blades infrastructure. I haven&#39;t had the opportunity to work directly with them but I guess they&#39;re similar to the N4K for IBM blades.</p>
      <p>Now I have a question that&#39;s not entirely related to the document but maybe you know the answer... when you deploy an HP environment with N5K+B22 and blade servers with an 2x embedded CNAs/blade, is the iSCSI acceleration available in the CNA to be used by the OS? (a vSphere5 hypervisor in this case). I&#39;m asking because it looks to me like in order to benefit from the iSCSI acceleration (or FCoE feature) on an HP FlexFabric CNA you need to use VirtualConnects and enable the FlexHBA on the 2nd PF. I know with FCoE there might not be a way around this, but what about iSCSI?... is it possible that the HW acceleration will be available even without the FlexHBA?</p>
      <p>BTW, are there EMC documents like there but on iSCSI?</p>
      <p>Thanks!<br />
      Alberto</p>
  - author: "Erik Smith"
    date: "02/29/2012 at 07:36 PM"
    html: |-
      <p>Thanks Alberto!  I checked with our HP Blade Server expert (Aditya) and he pointed out that we haven&#39;t qualified the B22 FEX modules yet.  As we are doing this work, we&#39;ll try and get you a better answer.  </p>
      <p>In regards to an EMC iSCSI TechBook, I don&#39;t know of one..  </p>
      <p>Erik </p>
---

<p>Over the past couple of months we’ve been working on adding some FCoE specific “Blade Server” information to the FCoE TechBook.&#0160; Actually the vast majority of the work was done by two of my colleagues, Aditya Nadkarni and Shreedhan Nikam (more about them later).</p>
<p>Early on in this process of adding this new material, we realized the sheer size of the FCoE TechBook (16MB!) was making it difficult to use as a quick reference and we set out to determine the best way to resolve this.&#0160; We ended up agreeing to create two separate FCoE TechBooks.</p>
<p>The first FCoE TechBook is “<a href="http://www.emc.com/collateral/hardware/technical-documentation/h6290-fibre-channel-over-ethernet-techbook.pdf" target="_self">Fibre Channel over Ethernet (FCoE) and Data Center Bridging (DCB) <strong>Concepts and Protocols</strong></a>”.&#0160; This techbook includes:</p>
<ul>
<li>An introduction to FCoE</li>
<li>A detailed FCoE and DCB theory of operation section</li>
<li>Supported topologies and products</li>
<li>Supported FCoE solutions </li>
<li>An FCoE troubleshooting section&#0160; </li>
</ul>
<p>The second FCoE TechBook is “<a href="http://www.emc.com/collateral/hardware/technical-documentation/h10524-fcoe-case-studies-tb.pdf" target="_self">Fibre Channel over Ethernet (FCoE) and Data Center Bridging (DCB) <strong>Case Studies</strong></a>”.&#0160; This techbook includes step-by-step instructions (in “bleeding eyeball detail”) to configure a number of supported configurations.&#0160; The exact configurations described are:</p>
<ul>
<li>Brocade 8000 - Direct Connect</li>
<li>Brocade DCX (FCoE 10-24) Blade – Direct Connect</li>
<li>Cisco Nexus 5000 – Direct Connect</li>
<li>Cisco Nexus 7000, 5000, MDS – Multi-hop FCoE </li>
<li>Cisco Nexus 5000, 2232PP – &#0160;vPC Straight-through</li>
<li>Cisco Nexus 5000, 4001I – vPC Cross-connect</li>
<li>Cisco Nexus 5000 – Host vPC Direct Connect</li>
<li>Blade Server case studies:
<ul>
<li>UCS</li>
<li>IBM BladeCenter</li>
<li>HP Virtual Connect FlexFabric and Flex-10</li>
</ul>
</li>
</ul>
<p>The Blade Server case studies have been added over the past few months and are worthy of special note.&#0160; Both Aditya and Shreedhan have managed to put together over 150 pages of detailed connectivity related installation instructions.&#0160; If you need to understand FCoE and its application in a Blade Server environment, I would highly recommend that you start here.</p>
<p>Thanks for reading!</p>
