---
title: "Creating SAN Port Channels when using NPV mode on Nexus 5k"
pubDate: 2010-12-20
postedAt: "11:40 AM"
description: "I received a question recently from Anthony Padula that asked if SAN Port Channels were supported on a Nexus 5000 running in NPV mode. After speaking with a few colleagues, locating the documentation, and setting it up in the lab, I am happy to say that the answer is yes!..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2010/12/creating-san-port-channels-when-using-npv-mode-on-nexus-5k.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250911170637/https://brasstacksblog.typepad.com/brass-tacks/2010/12/creating-san-port-channels-when-using-npv-mode-on-nexus-5k.html"
pdf: "/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/creating-san-port-channels-when-using-npv-mode-on-nexus-5k.pdf"
comments:
  - author: "Chris Carter"
    date: "12/20/2010 at 03:32 PM"
    html: |-
      <p>Thanks for information Erik.  Sounds like everything worked as it should, but nice to see verification of it in writing from a source I trust.</p>
  - author: "Sam"
    date: "03/07/2011 at 08:39 AM"
    html: |-
      <p>Very nice article Erik! Do you think NP SAN PortChannel is also possible with a Brocade upstream switch?</p>
  - author: "Erik Smith"
    date: "03/07/2011 at 09:39 AM"
    html: |-
      <p>Thanks!  No, I don&#39;t believe an NP Port-Channel would work with a Brocade upstream switch.  That having been said I haven&#39;t actually tried it...</p>
  - author: "Erik Smith"
    date: "05/17/2011 at 05:03 PM"
    html: |-
      <p>Errata: I&#39;m not sure why (yet) but while I was configuring this recently on a new 5596, I needed to add force when adding the channel-group to a set of interfaces.  </p>
      <p>The exact issue is in the &quot;SAN Port Channel 200 (Spo200)&quot; section.  Under the steps for configuring 5548-2, the line &quot;channel-group 200&quot; should be &quot;channel-group 200 force&quot;.     </p>
  - author: "kumar"
    date: "10/01/2011 at 11:53 AM"
    html: |-
      <p>Excellent post. </p>
      <p>On N5k side, do you have to configure the switch to either NPV mode of FC-SW mode?  There by restricting the switch to either act as a SAN switch or a traditional ethernet switch?</p>
      <p>I am wondering if one switch can be used for both your storage traffic and Ethernet traffic. </p>
  - author: "Erik Smith"
    date: "10/01/2011 at 05:56 PM"
    html: |-
      <p>Hi Kumar, Thanks!</p>
      <p>You can use either NPV mode or FC-SW mode to support FCoE.  Non-FCoE traffic will work the same in either of these modes.  </p>
      <p>On UCS, I believe there is also a feature that allows you to put the non-FCoE side of the Ethernet switch into either an NPV mode or a switch mode...</p>
---

<p>I received a <a href="https://web.archive.org/web/20250911170637/https://brasstacksblog.typepad.com/brass-tacks/2010/11/nexus-5000-2232pp-configuration.html?cid=6a013487ed263f970c0133f59f2015970b#comment-6a013487ed263f970c0133f59f2015970b" target="_self">question</a> recently from Anthony Padula that asked if SAN Port Channels were supported on a Nexus 5000 running in NPV mode.&#0160; After speaking with a few colleagues, locating the documentation, and setting it up in the lab, I am happy to say that the answer is yes!&#0160;</p>
<p>However, as usual, I found the documentation to be somewhat confusing and as a result, in this post I’m going to share the topology, caveats, and configuration steps that I used as well as the output from some helpful show commands.&#0160; I’m also going to include some information on the link failover testing that I performed.</p>
<p><strong><span style="text-decoration: underline;">Topology</span></strong></p>
<p>The topology that was configured is shown in the following diagram.</p>
<p><a href="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0148c6e867d1970c.jpg" style="display: inline;"><img alt="Topology" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0148c6e867d1970c image-full" src="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0148c6e867d1970c.jpg" title="Topology" /></a>&#0160;<br />&#0160;</p>
<p>The 9148 was running 5.0(1a) and the Nexus switches were all running 5.0(2)N1(1).</p>
<p><strong><span style="text-decoration: underline;">Caveats</span></strong></p>
<ul>
<li><strong>On the 9148, the “san-port-channel” interface is referred to a “port-channel”.&#0160; This can be confusing when configuring a SAN Port Channel between a Nexus 5k and an MDS.</strong></li>
<li><strong>The interface defaults for trunk mode are different on a Nexus 5k running in NPV mode than they are for a Nexus 5k running in FC-SW mode.&#0160; As a result, when you do a side-by-side comparison of the interfaces using “show run interface fc2/x”, the configurations will appear to be different.&#0160; Instead, use “show interface fc2/x” which allows you to determine how the port is actually configured and is not dependent on the default interface settings.</strong></li>
</ul>
<p><strong><span style="text-decoration: underline;">Setup steps</span></strong></p>
<p>The tables that follow provide a list of commands to use on each switch.&#0160; If you follow the steps in order, the SAN Port Channel should come up and not require additional configuration.</p>
<p><strong>SAN Port Channel 100 (Spo100)</strong></p>
<p>To configure Spo100, both the 9148 and the 5020 need to be configured as follows:</p>
<p style="text-align: center;"><a href="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0148c6e8695a970c.jpg" style="display: inline;"><img alt="Spo100" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0148c6e8695a970c" src="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0148c6e8695a970c.jpg" title="Spo100" /></a>&#0160;</p>
<p><strong>SAN Port Channel 200 (Spo200)</strong></p>
<p>To configure Spo200, both the 5020 and 5548-2 need to be configured as follows:</p>
<p style="text-align: center;"><a href="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0147e0de514e970b.jpg" style="display: inline;"><img alt="Spo200" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0147e0de514e970b" src="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0147e0de514e970b.jpg" title="Spo200" /></a>&#0160;<br />&#0160;</p>
<p><strong>SAN Port Channel 256 (Spo256)</strong></p>
<p>To configure Spo200, both the 5020 and 5548-2 need to be configured as follows:</p>
<p style="text-align: center;"><strong><a href="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0147e0de5210970b.jpg" style="display: inline;"><img alt="Spo256" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0147e0de5210970b" src="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0147e0de5210970b.jpg" title="Spo256" /></a>&#0160;<br />&#0160;</strong></p>
<p><strong><span style="text-decoration: underline;">Output from the show interface brief command</span></strong></p>
<p>When the commands above have been all been entered, the output from the show interface brief should appear as follows.</p>
<p><em>Note: The output has been truncated.</em>&#0160;</p>
<p><strong>MDS-9148</strong></p>
<p><strong><a href="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0148c6e86cdc970c.jpg" style="display: inline;"><img alt="Showintbrief_edited_9148" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0148c6e86cdc970c image-full" src="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0148c6e86cdc970c.jpg" title="Showintbrief_edited_9148" /></a>&#0160;<br /></strong><strong></strong></p>
<p><strong>Nexus-5020</strong></p>
<p><strong><a href="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0148c6e86d74970c.jpg" style="display: inline;"><img alt="Showintbrief_edited_5020" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0148c6e86d74970c image-full" src="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0148c6e86d74970c.jpg" title="Showintbrief_edited_5020" /></a>&#0160;<br /></strong></p>
<p><strong>Nexus-5548-1</strong></p>
<p><strong><a href="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0148c6e86df9970c.jpg" style="display: inline;"><img alt="Showintbrief_edited_5548-1" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0148c6e86df9970c image-full" src="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0148c6e86df9970c.jpg" title="Showintbrief_edited_5548-1" /></a>&#0160;<br /></strong></p>
<p><strong>Nexus-5548-2</strong></p>
<p><strong><a href="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0147e0de54b8970b.jpg" style="display: inline;"><img alt="Showintbrief_edited_5548-2" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0147e0de54b8970b image-full" src="/brasstacks/creating-san-port-channels-when-using-npv-mode-on-nexus-5k/6a013487ed263f970c0147e0de54b8970b.jpg" title="Showintbrief_edited_5548-2" /></a>&#0160;<br />&#0160;</strong></p>
<p><strong><span style="text-decoration: underline;">Observations from testing</span></strong></p>
<p>Once the SAN Port Channels were up, I checked connectivity to storage using INQ and started I/O using COPA.&#0160; In case you don’t know, INQ and COPA are two of EMC’s proprietary tools that are regularly used in the E-Lab.&#0160; Once I verified there weren’t any basic errors on the hosts or storage ports, I decided to run a couple of tests to see what kind of an impact the SAN Port Channel feature has on connectivity during a few failure scenarios.&#0160;</p>
<p>During each test, I used an xgig analyzer to monitor a couple of the CNAs that were using the SAN Port Channel to access storage.&#0160; Since I was physically pulling cables and expected many frames to be dropped during each test, I was more concerned with measuring the amount of time a host lost connectivity to storage, rather than the number of frames dropped while pulling a cable.&#0160; As a result, the analyzer was primarily being used to monitor the CNA’s throughput rather than capture, analyze, and characterize the disruption (e.g., number of frames dropped, etc).&#0160; Also, in all tests, the amount of bandwidth being used was less than the bandwidth available on any single member of the SAN Port Channel.&#0160; This was done to prevent the link from becoming oversubscribed during the testing and allowing congestion and backpressure to skew the test results.&#0160; For more information about congestion and backpressure, refer to the <em><a href="http://www.emc.com/collateral/hardware/technical-documentation/h4331-networked-storage-cncpts-prtcls-sol-gde.pdf" target="_self">Networked Storage Concepts and Protocols TechBook</a></em>.&#0160;&#0160;&#0160;&#0160;</p>
<p><strong>Single Link failover / failback</strong></p>
<p>With I/O running, I physically pulled the cable out of one of the switch interfaces that was a member of the SAN Port Channel.&#0160; I then reinserted the cable and after waiting for a few seconds, I pulled the other member of the SAN Port Channel and then pushed it back in.&#0160; I repeated this test a few times on all three SAN Port Channel configurations shown in the diagram above.&#0160; In all cases, the disruption was negligible and I saw virtually no drop in throughput via the xgig interface.&#0160; In addition, I was very happy with the improvement in behavior between the Nexus running in NPV mode and the 5020.&#0160; Previously, when removing one of the links between a switch running in NPV mode and its “core” switch, a number of the hosts would be logged out and then allowed to re-login via a different uplink to the core switch.&#0160; With the SAN Port Channel, as long as one of the member ports was active at all times, none of the hosts on the NPV switch were impacted.&#0160;&#0160;&#0160;&#0160;&#0160;</p>
<p><strong>All links in SAN Port Channel pull / push</strong></p>
<p>In this test, I physically pulled the cables out of all of the switch interfaces that were members of the SAN Port Channel.&#0160; As expected, while the cables were disconnected, all of the hosts using the SAN Port Channel lost connectivity to storage.&#0160; The interesting thing is what happened when I reconnected the cables.&#0160; The switch-to-switch TE_Port to TE_Port connections took about 20 seconds for the link to come back up.&#0160; This is not unexpected since an approximate 20-second delay is built into the FC-SW standard when bringing up an ISL.&#0160; If you are interested in more information about this delay, you can check out the <em><a href="http://www.emc.com/collateral/hardware/technical-documentation/h4331-networked-storage-cncpts-prtcls-sol-gde.pdf" target="_self">Networked Storage Concepts and Protocols TechBook</a></em>.&#0160; Surprisingly, the connection from the 5548 running in NPV mode to the 5020 took a similar amount of time to come up all the way.&#0160; I haven’t had a chance to dig into the reason for this yet, but I thought it would have been much shorter.&#0160;</p>
<p><strong>Conclusion</strong></p>
<p>Overall, I was impressed with the SAN Port Channel functionality and would use it in my environment, especially if I had switches in NPV mode.&#0160; I didn’t perform enough testing to be able to comment too much on the load balancing aspect of the feature, but I did notice that the load appeared to be equally distributed across both links.&#0160; As I continue to test with the feature, I’ll dedicate some time to giving you all updates.</p>
<p>As always, thank you for reading!</p>
