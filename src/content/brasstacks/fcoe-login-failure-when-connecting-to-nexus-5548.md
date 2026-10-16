---
title: "FCoE login failure when connecting to Nexus 5548"
pubDate: 2011-01-12
postedAt: "03:11 PM"
description: "A couple of months ago while we were installing our Nexus 5548s in the E-Lab, we noticed an FCoE login problem. Although we configured the 5548s in exactly the same manner described for the Nexus 5020 / 5010 in the FCoE TechBook, the FCoE ENodes would not log in. At..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2011/01/fcoe-login-failure-when-connecting-to-nexus-5548.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250911183205/https://brasstacksblog.typepad.com/brass-tacks/2011/01/fcoe-login-failure-when-connecting-to-nexus-5548.html"
pdf: "/brasstacks/fcoe-login-failure-when-connecting-to-nexus-5548/fcoe-login-failure-when-connecting-to-nexus-5548.pdf"
comments:
  - author: "zwliy"
    date: "09/09/2011 at 05:32 AM"
    html: |-
      <p>I&#39;m gonna share it in Facebook, this is really awesome</p>
  - author: "Ernesto Garcia"
    date: "10/27/2011 at 10:45 AM"
    html: |-
      <p>HI Erik,<br />
      Thanks for this great post.<br />
      We have been trying to connect Brocade 1020CNAs to Nexus 5548UP, but we haven’t been able to get them to work.<br />
      We have the QoS configuration in place, so this is not the problem in our case. I was wondering, what driver version are you using in your CNAs and what is the software version in your nexus?<br />
      The problem seems to be that during the dcbx negotiation between the CNAs and the nexus, they choose “Protocol: CIN” instead of CEE, therefore the FLOGI is failing.<br />
      Any help will be greatly appreciated.</p>
      <p>Thanks<br />
      Ernesto<br />
      </p>
  - author: "Erik Smith"
    date: "10/27/2011 at 11:06 AM"
    html: |-
      <p>Hi Ernesto, this sounds like the other interop problem that I found on the Nexus 5596 and is covered at the following: <a href="/brasstacks/interoperability-issue-between-brocade-cna-and-cisco-nexus-5596/" rel="nofollow">http://brasstacksblog.typepad.com/brass-tacks/2011/06/interoperability-issue-between-brocade-cna-and-cisco-nexus-5596.html</a></p>
      <p>Although I&#39;ve never actually observed this problem on the 5548, the issue is timing related and as a result it theoretically could happen on the 5548.</p>
  - author: "Austinjeremy"
    date: "11/29/2011 at 11:42 PM"
    html: |-
      <p>The above commands are still required as of 5.0(3)N2(2a)</p>
      <p>This is exactly what I typed:<br />
      system qos<br />
      service-policy type qos input fcoe-default-in-policy<br />
      service-policy type queuing input fcoe-default-in-policy<br />
      service-policy type queuing output fcoe-default-out-policy<br />
      service-policy type network-qos fcoe-default-nq-policy</p>
      <p>Also, this can be helpful:<br />
      <a href="http://www.cisco.com/en/US/docs/switches/datacenter/nexus5000/sw/troubleshooting/guide/n5K_ts_fcoe.html" rel="nofollow">http://www.cisco.com/en/US/docs/switches/datacenter/nexus5000/sw/troubleshooting/guide/n5K_ts_fcoe.html</a></p>
  - author: "Erik Smith"
    date: "12/02/2011 at 08:01 AM"
    html: |-
      <p>Hi thanks for the update and the link.  Based on what I&#39;ve heard recently, I don&#39;t believe Cisco is planning on changing this anytime soon.</p>
      <p>Regards, Erik  </p>
  - author: "Dat"
    date: "04/09/2012 at 04:43 PM"
    html: |-
      <p>Thanks a lot! It really helps me to resolve the issue.</p>
  - author: "Jim Ch"
    date: "06/09/2020 at 07:25 AM"
    html: |-
      <p>Thanks! Just bought one of these and am setting it up... if I hadn&#39;t seen this blog, who knows how many days I could have wasted trying to work out what was going on!</p>
---

<p>A couple of months ago while we were installing our Nexus 5548s in the E-Lab, we noticed an FCoE login problem. &#0160;Although we configured the 5548s in exactly the same manner described for the Nexus 5020 / 5010 in the FCoE TechBook, the FCoE ENodes would not log in.&#0160; At first we thought it was a problem with the ENodes, but an xgig trace showed that the 5548 was not transmitting any DCBX or FIP frames.&#0160; As a result, I sent an email off to my friends at Cisco that essentially asked “WTFF?” (Where’s The FIP Frames?).&#0160; A short time later, Cisco sent a message similar to &#0160;the following:</p>
<p><span style="color: #ff00ff;"><em>Hi Erik</em><em>,</em><em>&#0160;</em></span></p>
<p><span style="color: #ff00ff;"><em>QoS class-fcoe is not enabled by default on 5548 (to conserve buffers).&#0160; You should have seen a warning when you enabled feature fcoe.</em></span></p>
<p><span style="color: #ff00ff;"><strong><em>Switch(config)# feature fcoe</em></strong></span></p>
<p><span style="color: #ff00ff;"><strong><em>FC license checked out successfully</em></strong></span></p>
<p><span style="color: #ff00ff;"><strong><em>fc_plugin extracted successfully</em></strong></span></p>
<p><span style="color: #ff00ff;"><strong><em>FC plugin loaded successfully</em></strong></span></p>
<p><span style="color: #ff00ff;"><strong><em>FCoE manager enabled successfully</em></strong></span></p>
<p><span style="color: #ff00ff;"><strong><em>FC enabled on all modules successfully</em></strong></span></p>
<p><span style="color: #ff00ff;"><strong><em>Warning: Ensure class-fcoe is included in qos policy-maps of all types</em></strong></span></p>
<p><span style="color: #ff00ff;"><em>To accomplish this, attach these qos policies under system qos</em></span></p>
<p><span style="color: #ff00ff;"><em>**********************************************</em></span></p>
<p><span style="color: #ff00ff;"><em>switch (config-sys-qos)# service-policy type qos input</em></span></p>
<p><span style="color: #ff00ff;"><em>fcoe-default-in-policy</em></span></p>
<p><span style="color: #ff00ff;"><em>switch (config-sys-qos)# service-policy type queuing input</em></span></p>
<p><span style="color: #ff00ff;"><em>fcoe-default-in-policy</em></span></p>
<p><span style="color: #ff00ff;"><em>switch (config-sys-qos)# service-policy type queuing output</em></span></p>
<p><span style="color: #ff00ff;"><em>fcoe-default-out-policy</em></span></p>
<p><span style="color: #ff00ff;"><em>switch (config-sys-qos)# service-policy type network-qos</em></span></p>
<p><span style="color: #ff00ff;"><em>fcoe-default-nq-policy</em></span></p>
<p><span style="color: #ff00ff;"><em>**********************************************</em></span></p>
<p><span style="color: #ff00ff;"><em>Please run the above commands on the switch and let us know if that resolves your issue.</em></span></p>
<p><em><span style="color: #ff00ff;">This is also documented in the </span><a href="http://www.cisco.com/en/US/docs/switches/datacenter/nexus5000/sw/qos/502_n1_1/Cisco_Nexus_5000_Series_NX-OS_Quality_of_Service_Configuration_Guide_Rel_502_N1_1_chapter3.html#task_1135199" target="_self">Cisco QOS</a></em><a href="http://www.cisco.com/en/US/docs/switches/datacenter/nexus5000/sw/qos/502_n1_1/Cisco_Nexus_5000_Series_NX-OS_Quality_of_Service_Configuration_Guide_Rel_502_N1_1_chapter3.html#task_1135199" target="_self"> document</a>.</p>
<p>I ran the commands they provided and the ENodes immediately logged in.&#0160; I’ve since discussed the “Warning” message with Cisco and have encouraged them to consider providing a prompt to the user that would ask if they would like to automatically enable the appropriate service policy.</p>
<p>In any case, since the 5548 was added to the January EMC Support Matrix and the 5548 specific information will not be in the EMC FCoE TechBook until February, I wanted to make sure that these new QOS settings were clearly spelled out somewhere by EMC.&#0160;</p>
<p>Thanks for reading!</p>
