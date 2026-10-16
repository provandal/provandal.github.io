---
title: "Does FCoE require DCB Ethernet?"
pubDate: 2012-02-16
postedAt: "09:14 AM"
description: "I received a question earlier today that asked the following: \"I have heard some folks argue that ETS (Enhanced Transmission Selection) is NOT required to make FCoE work. I'm thinking specifically of the case in which a CNA is connected to a DCB-capable Ethernet switch that is doing FIP Snooping,..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2012/02/does-fcoe-require-dcb-ethernet.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250911162609/https://brasstacksblog.typepad.com/brass-tacks/2012/02/does-fcoe-require-dcb-ethernet.html"
pdf: "/brasstacks/does-fcoe-require-dcb-ethernet/does-fcoe-require-dcb-ethernet.pdf"
comments:
  - author: "Victor"
    date: "02/16/2012 at 09:49 AM"
    html: |-
      <p>Erik, thank you for that thorough answer. Brilliant, as usual. If it&#39;s OK, I would like to add another component to the answer: the popular view. From talking to industry data center architects, in particular those who manage high-performance environments, I think the prevailing view is that FCoE requires DCB to provide a lossless environment and any switch that does not offer ETS will be summarily rejected as an inadequate solution that can place the environment at risk.</p>
      <p>Has that been your experience, too?</p>
      <p>Digging a bit on the technical side of ETS, my understanding is that ETS does not only provide guaranteed BW, which one can configure today with legacy QoS tools, like Cisco&#39;s MQC, but that it will allow a statistical multiplexing type model on top of that. In that model, the traffic types that fall under the ETS Traffic Class (TC-2) and are scheduled according to the ETA algorithm (which I know is not specified in the standard - usually its WRR) will not only be guaranteed a configured BW percentage of the link, but will also be able to have more BW DYNAMICALLY assigned to them as the offered load of the other traffic type drops/fluctuates. </p>
      <p>For example, in a scenario in which I have LAN and SAN traffic under the ETS Traffic Class, and the LAN traffic is assigned 60% of the BW and the SAN 40%, that means on a 10G link, the LAN gets 6G and the SAN gets 4G guaranteed. HOWEVER, as I understand the technology, each traffic type will be able to exceed that guaranteed amount of 60 and 40 IF the other traffic class&#39;s offered load does not meet its minimum. So, if at time t1, the LAN traffic&#39;s offered load is only 2G, not 6G, and the SAN traffic needs to burst, ETS will schedule the SAN traffic such that it can use the 4G that the LAN traffic is not using at that particular time. In short, each traffic type can use the other&#39;s BW if they&#39;re not using it at a particular type. This is done dynamically.</p>
      <p>Is this your understanding of what ETS is and what it does?</p>
  - author: "Erik Smith"
    date: "02/16/2012 at 10:10 AM"
    html: |-
      <p>Hi Victor, thanks!  Your description matches my understanding of ETS.  There&#39;s a little bit of additional information in the EMC FCoE TechBook if you&#39;re interested.</p>
  - author: "Victor"
    date: "02/16/2012 at 10:18 AM"
    html: |-
      <p>Thanks, my good man. </p>
  - author: "Erwin van Londen"
    date: "03/15/2012 at 02:12 AM"
    html: |-
      <p>Hi Eric,</p>
      <p>I agree. The resilience and reliability of FC has caused a lack of interest (or shortage of development resources, depends how you look at it) in the ULP side of the protocols like SCSI. The networking peeps have eliminated this by building a very resilient routable framework on top of that called TCP/IP. :-) </p>
      <p>For this reason SCSI works on TCP/IP but not ethernet. Hence the invention of FCoE. :-)</p>
      <p>If you leave out DCB, ETS and PFC I would argue you will find yourself on very thin ice when trying to push channel protocols through a CNA.</p>
      <p>Regards,<br />
      Erwin</p>
  - author: "Erik Smith"
    date: "03/15/2012 at 08:32 AM"
    html: |-
      <p>Hi Erwin, I agree.  TCP/IP provides a reliable transport and that block I/O protocols (perhaps most protocols that utilize TCP) require a lossless or seemingly lossless transport in order to function properly.</p>
      <p>Regards, Erik   </p>
  - author: "Simon Gordon"
    date: "05/19/2012 at 02:28 AM"
    html: |-
      <p>As you say all devices in practice require DCBX and pfc to get running by default, some have manual override to allow configuration override something that was in the draft dcb standards but not in the final version.  Some but not all devices require ets to e configured as well.  Practically the same qos can be achieved without ets through normal l2 cos at the priority level (ets being at the group of priority levels - something many people forget). However in reality I 100% agree with your position that the best practice is clearly DCBX PFC and ETS (and FIP Sooping on any L2 switch).</p>
  - author: "jason"
    date: "04/28/2014 at 11:48 PM"
    html: |-
      <p>Hi,Does VN2VN FCoE require DCB Ethernet? and how to config it?</p>
  - author: "Erik Smith"
    date: "04/29/2014 at 08:52 AM"
    html: |-
      <p>Hi Jason, all (FC-BB-5 and FC-BB-6) variations of FCoE require a lossless transport, so yes DCB Ethernet is a requirement with VN2VN.  </p>
      <p>How you configure support for VN2VN is platform dependent.  Which CNA, DCB capable switch and Storage plaform are you planning to use?</p>
---

<p>I received a question earlier today that asked the following:</p>
<p><em><span style="font-family: comic sans ms,sans-serif; font-size: 12pt;">&quot;I have heard some folks argue that ETS (Enhanced Transmission&#0160;Selection) is NOT required to make FCoE work. I&#39;m thinking specifically of the case in which a CNA is connected to a DCB-capable Ethernet switch that is doing FIP Snooping, which is then uplinked to, say, a&#0160;Cisco Nexus. The argument goes that the DCB-capable switch does NOT require ETS support to make this design work and be stable - supporting PFC would be enough.</span></em><br /><br /><em><span style="font-family: comic sans ms,sans-serif; font-size: 12pt;">What do you think of that?&quot;</span></em></p>
<p>I have two different answers; a practical one and then a theoretical one.</p>
<h3><strong>Practical </strong></h3>
<p>From a practical point of view, I wouldn’t even consider using a FIP Snooping Bridge, ENode or FCF that does not support PFC, ETS and DCBX.&#0160; To figure out why, you’ll need to read the theoretical answer…</p>
<h3>Theoretical</h3>
<p>From a theoretical point of view, the FCoE protocol can actually function without any DCB features (i.e., DCBX, PFC, ETS), it just won’t allow the ULP (SCSI-FCP) to work very efficiently.&#0160; By this I mean the driver supporting the ULP would spend a significant portion of its time in error recovery (because of frame loss due to normal periodic congestion in the Ethernet network) rather than doing useful work.&#0160; This is specifically a problem for SCSI-FCP, because it “evolved” in a lossless environment (FC / BB_Credit) and as a result no significant amount of work was done on a retransmit like mechanism.&#0160; In other words, since frame loss happens so infrequently in FC, the easiest (and cheapest) way to recover from a frame loss is to retry the entire exchange.&#0160;</p>
<p>When attempting to run FC / SCSI-FCP directly over Ethernet, as is done with FCoE, the solution to the frame loss problem is to make the Ethernet link lossless, which means that some form of Pause will need to be used.&#0160; You could use either Pause (802.3x – a.k.a Link Pause) or Priority Flow Control (PFC – 802.1Qbb).&#0160; The problem with using “Link Pause” is that it pauses the entire link.&#0160; Since one of the main selling points of FCoE is to converge the network, this means that multiple traffic types will usually be present when FCoE is in use.&#0160; When Pause is used in this type of environment, all traffic using the link will also be paused.&#0160; This behavior presents a significant problem because it can cause congestion spreading and I believe it could get in the way of TCPs flow control mechanism because no frames will be dropped.&#0160; The solution is to use PFC.&#0160; When using PFC, FCoE traffic can be lossless and other types of traffic can remain lossy.</p>
<p>With the above in mind, ETS is needed to ensure that lossy and lossless traffic are each guaranteed a certain amount of bandwidth.&#0160; Is it strictly required to enable FCoE to function?&#0160; No!</p>
<p>Then there is DCBX which isn’t required to allow FCoE to function properly either, but it does allow for the ENodes (CNAs) to be properly configured (automatically) to use the DCB settings defined on the switch.&#0160; This prevents misconfiguration of the ENodes and it makes life easier for the end user.&#0160;&#0160;</p>
<p>All of this is interesting from a theoretical point of view, but as I said previously in practice, I wouldn’t even think about using an ENode or an FCF that didn’t support DCBX, PFC, ETS.&#0160; These DCB extensions should be considered required in order to make FCoE reliable and easy to use.&#0160; As a side note, these extensions are also supported by all of the FCoE implementations I am aware of, so we really don’t have a choice anyway…</p>
<p>Thanks for reading!</p>
