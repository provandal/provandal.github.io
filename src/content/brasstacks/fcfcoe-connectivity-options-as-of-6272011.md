---
title: "FC/FCoE Connectivity options as of 6/27/2011"
pubDate: 2011-06-27
postedAt: "02:56 PM"
description: "About a month ago I received an email from someone asking \"When will the FCoE Tech Book be updated to properly reflect EMCs support for native FCoE on our arrays?\" My initial reaction was \"OH!, <golly-gee>\" and then the inevitable\"Of all the <interesting> pieces of information to <absentmindedly> leave out\"...."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2011/06/fcfcoe-connectivity-options-as-of-6272011.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250911143420/https://brasstacksblog.typepad.com/brass-tacks/2011/06/fcfcoe-connectivity-options-as-of-6272011.html"
pdf: "/brasstacks/fcfcoe-connectivity-options-as-of-6272011/fcfcoe-connectivity-options-as-of-6272011.pdf"
comments:
  - author: "Zappom"
    date: "06/28/2011 at 03:51 AM"
    html: |-
      <p>Hi Erik, <br />
      excellent and very handy Plattform to see very fast what works.<br />
      Chapeau... </p>
  - author: "Erik Smith"
    date: "06/28/2011 at 07:47 AM"
    html: |-
      <p>Thanks!  </p>
  - author: "Otto le Roux"
    date: "06/29/2011 at 05:12 PM"
    html: |-
      <p>Awesome work, thanks mate. This is going to be very useful.</p>
  - author: "Jerry Liu"
    date: "08/12/2011 at 03:34 AM"
    html: |-
      <p>Hi, Erik,</p>
      <p>Does Brocade DCX support AG mode?</p>
      <p>Jerry</p>
  - author: "Erik Smith"
    date: "08/19/2011 at 04:05 PM"
    html: |-
      <p>Hi Jerry, apologies for the delayed response, somehow I missed your comment.  </p>
      <p>No they don&#39;t support AG mode on the DCX.  If you try to do this you will get the following error message.</p>
      <p>DCSwitch:admin&gt; ag --modeenable<br />
      Access Gateway mode is not supported on this platform<br />
      DCSwitch:admin&gt;<br />
      </p>
  - author: "Shanon R Lawton"
    date: "09/29/2011 at 06:37 PM"
    html: |-
      <p>Erik, is eLab testing the Nexus 7K and MDS FCoE line cards as well? </p>
  - author: "Erik Smith"
    date: "09/30/2011 at 07:36 PM"
    html: |-
      <p>Hi Shanon, yes we&#39;re in the process of testing FCoE on N7K now.  We were due to release support for it in the October ESM but we ran into an issue that prevented us from completing testing by the ESM (EMC Support Matrix) cut-off date.  </p>
      <p>The problem turned out to be relatively minor and I hope to provide a post next week that will describe the issue.  </p>
      <p>In November we&#39;re planning to add an N7k case study to the FCoE tech book and I&#39;ll be updating my &quot;supported FCoE Topologies&quot; blog post at the same time.  </p>
  - author: "dika"
    date: "11/02/2012 at 03:28 AM"
    html: |-
      <p>Hi Erik, nice share. very usefull post.</p>
      <p>it could be more helpfull if u would to show me the configuration FCoE at nexus 5000 connect to UCS via Nexus 2000. im confused where i should bind my vfc interface, i already bind at nexus 2000 interface eth101/1/1 but my ucs pwwwn doesnt show at flogi database.</p>
      <p>im very thankfull if u response my questions.</p>
      <p>regards</p>
  - author: "Erik"
    date: "11/09/2012 at 08:13 AM"
    html: |-
      <p>Hi Dika, apologies for the delayed response, I received a burst of spam comments about the same time as yours and I didn&#39;t notice your comment until just now.  </p>
      <p>We did put together a UCS specific case study, but I&#39;m not sure it included the Nexus 2k.  Take a look at the following and if you don&#39;t find what you need let me know.  <a href="http://www.emc.com/collateral/hardware/technical-documentation/h10524-fcoe-case-studies-tb.pdf" rel="nofollow">http://www.emc.com/collateral/hardware/technical-documentation/h10524-fcoe-case-studies-tb.pdf</a></p>
  - author: "John Law"
    date: "04/17/2013 at 06:16 AM"
    html: |-
      <p>Hi, Erik, does Cisco 4001i support direct attached with native FCoE storage?  That means Nexus 5000 series switches did not required between 4001i and FCoE storage. </p>
  - author: "Erik"
    date: "05/01/2013 at 07:35 PM"
    html: |-
      <p>Hi John, unfortunately no.  The 4001i must be connected to a Nexus 5k in order for the FCoE virtual links to be formed.</p>
      <p>Regards, Erik </p>
---

<p>About a month ago I received an email from someone&#0160;asking &quot;When will the <a href="http://www.emc.com/collateral/hardware/technical-documentation/h6290-fibre-channel-over-ethernet-techbook.pdf" target="_self">FCoE Tech Book</a>&#0160;be updated to properly reflect EMCs support for native FCoE on our arrays?&quot;&#0160;</p>
<p>My initial reaction was &quot;OH!,&#0160;&lt;golly-gee&gt;&quot;&#0160;and then the inevitable&quot;Of all the &lt;interesting&gt; pieces of information to &lt;absentmindedly&gt; leave out&quot;.&#0160; &#0160;</p>
<p>My actual response was &quot;what format would you like to see the options presented in?&quot;</p>
<p>In response, they provided a link to <a href="http://virtualeverything.wordpress.com/2010/07/02/valid-cisco-based-fc-fcoe-combinations-as-of-722010/" target="_self">a blog post on virtualeverything</a>&#0160;and said “it would be really nice if you could do the same for EMC Storage.”&#0160;</p>
<p>After looking at&#0160;the format of the blog post&#0160;referenced, I completely agreed and decided to copy it.&#0160; I also decided to add Brocade FCoE information as well as a list of configuration rules to hopefully avoid the “why don’t you support x with y” types of questions.&#0160; That having been said, if you have any questions, please let me know.&#0160;</p>
<p>I intend to update the configuration rules and diagrams on an as needed basis.</p>
<h2>Configuration rules</h2>
<p>The following configuration rules were used to create the topology diagrams.&#0160; If there is a discrepancy between the diagrams and the configuration rules, the configuration rules take precedence:</p>
<ol>
<li>The Nexus 2232 requires a connection to a Nexus 5000 in order to function.</li>
<li>The Nexus 2232 does not support native Fibre Channel ports.</li>
<li>The Nexus 4001i requires a connection to a Nexus 5000 in order to support FCoE.</li>
<li>The Nexus 4001i does not support native Fibre Channel ports.</li>
<li>The Nexus 7000 does not support native Fibre Channel ports.</li>
<li>The Fibre Channel ports on the Nexus 5000 cannot be used for end device connectivity while the switch is in NPV mode.</li>
<li>FC-SW interoperability between Brocade and Cisco is not supported.&#0160; When attaching a Brocade switch to a Cisco FCF and vice versa, either NPV mode must be used on the Cisco switch or AG mode must be used on the Brocade switch.</li>
<li>The Fibre Channel ports on the Brocade 8000 cannot be used for end device connectivity while the switch is in NPV mode.</li>
<li>All host connectivity to the UCS 6100 is via FCoE.</li>
<li>The Fibre Channel ports on the UCS 6100 cannot be used for end device connectivity while the switch is in NPV mode.</li>
<li>The UCS 6100 does not currently provide an FC zoning interface.&#0160; As a result, when the 6100 is running in FC-SW mode, it must be connected to another Cisco switch that is also running in switch mode.</li>
<li>Cascading switches that are running in NPV / AG mode is not supported.</li>
<li>The Nexus 4001i does not support external VN_Port connections</li>
<li>EMC does not currently support FCoE on the Nexus 7000 or MDS.&#0160; We expect to release support for this in September.</li>
<li>Storage ports cannot be connected to the Nexus 5000 while it is running in NPV mode.</li>
<li>The Brocade 8000 and DCX do not support VE_Ports</li>
<li>Cisco UCS does not currently support VE_Ports.</li>
<li>FCoE NPV uplinks between Cisco and Brocade switches are not supported.</li>
<li>VN_Port to VN_Port connections (a host&#0160;directly&#0160;connected to storage) without the use of an FCF is not supported with FC-BB-5.&#0160;</li>
</ol>
<h2>Supported connectivity options:</h2>
<p>The supported connectivity options have been broken down into several categories.&#0160;&#0160;Each category focuses on the connectivity options for a particular connectivity component.&#0160; The categories are:</p>
<ol>
<li>Configurations specific to Nexus 5000</li>
<li>Configurations specific to Nexus 2000</li>
<li>Configurations specific to Nexus 4001i</li>
<li>Configurations specific to Nexus 6100</li>
<li>Configurations specific to MDS</li>
<li>Configurations specific to Brocade 8000 / DCX</li>
</ol>
<h2>Configurations specific to Nexus 5000:</h2>
<p>Please note:&#0160; The first configuration shown is not specific to the 5000.&#0160; It&#0160;has been included to call your attention to the fact that native FC supports a host being directly connected to storage but FCoE does not.</p>
<p><a href="/brasstacks/fcfcoe-connectivity-options-as-of-6272011/6a013487ed263f970c01538f7a1a92970b.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01538f7a1a92970b image-full" src="/brasstacks/fcfcoe-connectivity-options-as-of-6272011/6a013487ed263f970c01538f7a1a92970b.jpg" title="One" /></a>&#0160;&#0160;</p>
<h2><em>Configurations specific to Nexus 2000:</em></h2>
<p><a href="/brasstacks/fcfcoe-connectivity-options-as-of-6272011/6a013487ed263f970c014e896d7baf970d.jpg" style="display: inline;"><img alt="Two" border="0" class="asset  asset-image at-xid-6a013487ed263f970c014e896d7baf970d image-full" src="/brasstacks/fcfcoe-connectivity-options-as-of-6272011/6a013487ed263f970c014e896d7baf970d.jpg" title="Two" /></a>&#0160;</p>
<h2><em>Configurations specific to Nexus 4001i:</em></h2>
<p><a href="/brasstacks/fcfcoe-connectivity-options-as-of-6272011/6a013487ed263f970c0154334d8220970c.jpg" style="display: inline;"><img alt="Three" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0154334d8220970c image-full" src="/brasstacks/fcfcoe-connectivity-options-as-of-6272011/6a013487ed263f970c0154334d8220970c.jpg" title="Three" /></a>&#0160;</p>
<h2><em>Configurations specific to 6100:</em></h2>
<p><a href="/brasstacks/fcfcoe-connectivity-options-as-of-6272011/6a013487ed263f970c014e896d7dcb970d.jpg" style="display: inline;"><img alt="Four" border="0" class="asset  asset-image at-xid-6a013487ed263f970c014e896d7dcb970d image-full" src="/brasstacks/fcfcoe-connectivity-options-as-of-6272011/6a013487ed263f970c014e896d7dcb970d.jpg" title="Four" /></a>&#0160;</p>
<h2><em>Configurations specific to MDS:</em></h2>
<p><a href="/brasstacks/fcfcoe-connectivity-options-as-of-6272011/6a013487ed263f970c01538f7a1e6f970b.jpg" style="display: inline;"><img alt="Five" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01538f7a1e6f970b image-full" src="/brasstacks/fcfcoe-connectivity-options-as-of-6272011/6a013487ed263f970c01538f7a1e6f970b.jpg" title="Five" /></a>&#0160;</p>
<h2><em>Configurations specific to Brocade 8000 / DCX:</em></h2>
<p><a href="/brasstacks/fcfcoe-connectivity-options-as-of-6272011/6a013487ed263f970c0154334d83ba970c.jpg" style="display: inline;"><img alt="Six" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0154334d83ba970c image-full" src="/brasstacks/fcfcoe-connectivity-options-as-of-6272011/6a013487ed263f970c0154334d83ba970c.jpg" title="Six" /></a>&#0160;</p>
<p>Thanks for reading!</p>
