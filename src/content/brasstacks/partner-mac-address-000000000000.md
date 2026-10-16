---
title: "Partner Mac Address: 00:00:00:00:00:00"
pubDate: 2012-01-29
postedAt: "06:58 PM"
description: "While setting up bonding on a Linux host running SLES 11, a colleague and I noticed that the output from cat /proc/net/bonding/bond0 showed a “Partner Mac Address:” of 00:00:00:00:00:00. (BTW, we’ve also observed this symptom on at least one other distro (Debian)). We were interested in the Partner MAC Address..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2012/01/partner-mac-address-000000000000.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250910180338/https://brasstacksblog.typepad.com/brass-tacks/2012/01/partner-mac-address-000000000000.html"
pdf: "/brasstacks/partner-mac-address-000000000000/partner-mac-address-000000000000.pdf"
comments:
  - author: "Waldemar Pera"
    date: "01/30/2012 at 06:34 AM"
    html: |-
      <p>By default, channel-group mode is On without LACP. If you enable globally LACP and set channel-group to Active, everything is ok. (<a href="http://www.cisco.com/en/US/docs/switches/datacenter/nexus5000/sw/configuration/guide/cli/EtherChannel.html)." rel="nofollow">http://www.cisco.com/en/US/docs/switches/datacenter/nexus5000/sw/configuration/guide/cli/EtherChannel.html).</a></p>
      <p>Another workaround, it&#39;s off LACP on Linux side.</p>
  - author: "Erik Smith"
    date: "01/30/2012 at 07:53 AM"
    html: |-
      <p>Hi Waldemar, that link is a great reference and I probably should have included a couple of switch configuration references in my originl post.</p>
      <p>However, the point of the blog post was to explain why the Partner MAC Address was zero and (to me at least) the link between LACP and this field was not immediately apparent.  Based on the feedback I&#39;ve already received, it seems like I may be in the minority here!</p>
      <p>Thanks for taking the time to comment!</p>
      <p>Erik </p>
  - author: "Kevin Joubert"
    date: "02/06/2013 at 05:14 PM"
    html: |-
      <p>Is the &quot;Partner MAC Address&quot; sort of a virtual hardware address for the connection pair?  I have a strange situation where two systems are showing the same Partner MAC Address on their respective bond0 interfaces. I am thinking that  these somehow the 4 ports (2 connections in each bond0 on each server) are portchanneled together.. and they shouldn&#39;t be I don&#39;t think. </p>
  - author: "Erik"
    date: "02/11/2013 at 10:09 AM"
    html: |-
      <p>Hi Kevin, I believe the Partner MAC Address is the MAC Address of the switch or switch  pair that you are connecting to.  If I noticed the same Partner MAC Address on two different servers that were connected to the same switch / switch pair, I wouldn&#39;t be concerned...  </p>
---

<p>While setting up bonding on a Linux host running SLES 11, a colleague and I noticed that the output from <strong>cat /proc/net/bonding/bond0</strong> showed a “Partner Mac Address:”&#0160; of 00:00:00:00:00:00. (BTW, we’ve also observed this symptom on at least one other distro (Debian)).&#0160; We were interested in the Partner MAC Address field because we were trying to troubleshoot a connectivity issue and we thought (I believe mistakenly) that this was an indication of some kind of configuration problem on the switch.&#0160; It turns out that this symptom <span style="text-decoration: underline;">is</span> related to a switch configuration parameter and the short&#0160;answer&#0160;is: <strong>check to make sure that you have set the port-channel on the switch to “mode active”</strong>.&#0160;</p>
<p>For a more detailed explanation, please read on.&#0160;</p>
<h2><strong>Bonding overview</strong></h2>
<p>Before I dive into the details, a brief description of bonding would probably be helpful.&#0160; Bonding (known as NIC Teaming in windows environments) allows for two separate physical interfaces to be treated as a single logical interface.&#0160; There are a number of different ways to use bonding, so for the sake of this example, I am going to assume we want to use Active/Active.&#0160; More specifically&#0160;we are&#0160;going to use the setting “mode=802.3ad miimon=100”.&#0160; For more information about bonding, I highly recommend that you&#0160;review <a href="http://www.linuxfoundation.org/collaborate/workgroups/networking/bonding" target="_self">the bonding section of the linux foundation website</a> .</p>
<h2>Topology</h2>
<p>The approximate physical topology&#0160;we had configured in the lab is shown below:</p>
<p><a href="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c0168e650cb98970c.jpg" style="display: inline;"><img alt="Topology" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0168e650cb98970c image-full" src="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c0168e650cb98970c.jpg" title="Topology" /></a></p>
<p>The bonding configuration on the host that can be found in <strong>/etc/sysconfig/network/ifcfg-bond0</strong> was as follows:</p>
<p><a href="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c01630059ee01970d.jpg" style="display: inline;"><img alt="Output1" border="0" class="asset  asset-image at-xid-6a013487ed263f970c01630059ee01970d image-full" src="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c01630059ee01970d.jpg" title="Output1" /></a>&#0160;</p>
<p>And the current status of the bond as found via <strong>cat /proc/net/bonding/bond0</strong> was:</p>
<p><a href="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c0167614fa116970b.jpg" style="display: inline;"><img alt="Output2" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0167614fa116970b image-full" src="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c0167614fa116970b.jpg" title="Output2" /></a>&#0160;</p>
<p>When we noticed this, we weren’t sure if a Partner Mac Address of all zeros was a problem or not but we were able to ping other devices that could only be accessed via the bond interface.&#0160; The question was, were both interfaces up and part of the bond, or not?&#0160;</p>
<p>The first way we thought to verify this was to use <strong>tcpdump –i bond0</strong> and compare the traffic on the newly configured bond with a known working bond on another host.&#0160; When we did this, we noticed there were lots of LACP frames being exchanged between the host and the switch in the known working configuration and there weren’t any LACP frames being exchanged between the host and the switches we were having problems with.&#0160;</p>
<p>Next, we reviewed the configurations from both of the Cisco switches in our topology and&#0160;verified&#0160;that they were the same:</p>
<p><a href="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c0168e650eb07970c.jpg" style="display: inline;"><img alt="Output3" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0168e650eb07970c image-full" src="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c0168e650eb07970c.jpg" title="Output3" /></a>&#0160;</p>
<p>Next, we reviewed the mac address table on both of the Nexus switches using <strong>show mac address-table</strong>.</p>
<p><a href="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c0167614fbd3e970b.jpg" style="display: inline;"><img alt="Output4" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0167614fbd3e970b image-full" src="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c0167614fbd3e970b.jpg" title="Output4" /></a>&#0160;</p>
<p>Since the same host MAC Address was shown in both tables, we came to the conclusion that the bond was working properly.&#0160;However, we&#0160;were still curious about the Partner MAC Address value, so on a hunch we changed the switch interface configuration so that both members would be using <strong>mode active</strong></p>
<p><a href="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c0168e6511010970c.jpg" style="display: inline;"><img alt="Output5" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0168e6511010970c image-full" src="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c0168e6511010970c.jpg" title="Output5" /></a></p>
<p>and the Partner MAC Address was now properly populated&#0160;</p>
<p><a href="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c0163005a23b6970d.jpg" style="display: inline;"><img alt="Output6" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0163005a23b6970d image-full" src="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c0163005a23b6970d.jpg" title="Output6" /></a></p>
<p>To get to the bottom of where the Partner MAC Address value was coming from, we took an xgig trace of the bond initializing both with and without &quot;mode active&quot;.&#0160; After reviewing the trace, it appears that server pulls the Partner MAC Address&#0160;out of&#0160;the LACP frames from the switch, see below</p>
<p><a href="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c0167614fd711970b.jpg" style="display: inline;"><img alt="Xgig" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0167614fd711970b image-full" src="/brasstacks/partner-mac-address-000000000000/6a013487ed263f970c0167614fd711970b.jpg" title="Xgig" /></a></p>
<p>In the case where the Partner MAC Address is set to zero, the port-channel is set to “mode on” and the switch doesn’t transmit any LACP frames.&#0160; As a result the server is unable to populate this field.&#0160;</p>
<p>I don’t believe there is a problem either way but at least now you’ll have a basic idea of why the Partner MAC Address is zero if you’re ever wondering.</p>
<p>Thanks for reading!</p>
