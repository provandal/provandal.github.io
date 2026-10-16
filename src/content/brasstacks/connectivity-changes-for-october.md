---
title: "Connectivity Changes for October"
pubDate: 2010-10-11
postedAt: "08:50 PM"
description: "In my previous post I wrote about documentation and how it can make your life miserable when it’s missing, or worse, inadequate. Oddly enough, the opposite is also true! Having too much documentation, especially when you are looking for a specific piece of information, can also make your life miserable…..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2010/10/connectivity-changes-for-october.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250914095734/https://brasstacksblog.typepad.com/brass-tacks/2010/10/connectivity-changes-for-october.html"
pdf: "/brasstacks/connectivity-changes-for-october/connectivity-changes-for-october.pdf"
comments: []
---

<p>In my previous post I wrote about documentation and how it can make your life miserable when it’s missing, or worse, inadequate.&#0160; Oddly enough, the opposite is also true!&#0160; Having too much documentation, especially when you are looking for a specific <span style="text-decoration: underline;">piece</span> of information, can also make your life miserable…&#0160;</p>
<p>For example, let’s say that you want to know when native FCoE support is going to be released for the EMC CLARiiON Storage Array or when the E-Lab connectivity team will be finished testing EOS 9.09.08 firmware.&#0160; Today you’d have no choice but to periodically check the EMC Support Matrix (ESM) or the E-Lab Navigator.&#0160; The obvious problem with this approach is that it is time consuming and requires some action on your part.&#0160; This usually isn’t a big deal since you will have to consult the ESM to find out exactly what configurations are supported anyway.&#0160; However, instead of periodically checking the ESM to look for changes, wouldn’t it be nice to get an automatic notification whenever something changes?&#0160;</p>
<p>I think it would…&#0160;</p>
<p>As a result, I’m going to start providing connectivity related updates on a monthly basis.&#0160; These “connectivity updates” will be posted as soon as possible after the publication of the ESM.&#0160; The updates will only deal with connectivity related items such as FC/FCoE switch firmware revisions, new features / topologies and updates to our documentation.&#0160; It’s important to note that I am not planning on providing updates that are host platform, OS or driver specific.&#0160; Also, I’m only going to provide a summary, so you’ll still need to read the release notes and check E-Lab navigator for the details.&#0160; However, at least you’ll know something has changed or become available and that you may want to review the appropriate documentation.</p>
<p>With this objective in mind, the connectivity updates for the month of October are listed below:</p>
<p><strong><span style="text-decoration: underline;">Native FCoE</span></strong></p>
<p style="padding-left: 30px;"><strong>Native FCoE support for CLARiiON</strong></p>
<ul style="padding-left: 30px;">
<li>The models listed in the ESM are the CX4-120FCoE, CX4-240FCoE, CX4-480FCoE and CX4-960FCoE</li>
<li>Support for FCoE requires at least 2 FCoE 10GbE SLICs and Release 30+</li>
<li>Maximum of two SLICs in CX4-120 and CX4-240</li>
<li>Maximum of four SLICs in CX4-480 and CX4-960</li>
<li>The supported Operating Systems consist of Windows, Linux and ESX&#0160; </li>
</ul>
<p><strong><span style="text-decoration: underline;">&#0160;</span></strong></p>
<p><strong><span style="text-decoration: underline;">Brocade</span></strong> (Courtesy of Aditya Nadkarni)</p>
<p style="padding-left: 30px;"><strong>Firmware changes in the October ESM:</strong></p>
<ul style="padding-left: 30px;">
<li>Brocade M-series (Legacy McDATA) EOS firmware version 9.09.08</li>
<li>FOS version v6.3.2a</li>
<li>FC-SW Interop support added between v6.4.0b and EOS 9.09.05 / 9.09.08</li>
<li>FC-SW Interop support added between v6.4.0b and NX-OS 5.0.1a.</li>
</ul>
<p style="padding-left: 30px;"><strong>Hardware changes in the October ESM:</strong></p>
<ul style="padding-left: 30px;">
<li>Two new NPIV gateways added<ol>
<li>HP 8Gb Virtual Connect FC module (572018-B21)</li>
<li>Dell 8Gb Brocade Access Gateway (only) module (M5424-n)</li>
</ol></li>
</ul>
<p><strong><span style="text-decoration: underline;">&#0160;</span></strong></p>
<p><strong><span style="text-decoration: underline;">Cisco</span></strong></p>
<p style="padding-left: 30px;"><strong>Firmware changes in the October ESM:</strong></p>
<ul style="padding-left: 30px;">
<li>NX-OS version 4.2(1)N2(1)</li>
</ul>
<p><strong><span style="text-decoration: underline;">&#0160;</span></strong></p>
<p><strong><span style="text-decoration: underline;">FCoE tech book</span></strong></p>
<p style="padding-left: 30px;"><strong>Nexus 5000 / 2232</strong></p>
<ul style="padding-left: 30px;">
<li>Nexus 2232PP overview section added</li>
<li>Nexus 5000 / 2232 reference topology and setup steps added</li>
</ul>
<p style="padding-left: 30px;"><strong>Brocade 8000 </strong>(Courtesy of Erik Paine)<strong></strong></p>
<ul>
<li>Setup steps for configuring Access Gateway mode on the 8000 added</li>
</ul>
