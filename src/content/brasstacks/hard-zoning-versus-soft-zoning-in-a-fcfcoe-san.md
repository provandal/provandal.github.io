---
title: "Hard zoning versus soft zoning in a FC/FCoE SAN"
pubDate: 2012-01-14
postedAt: "07:03 PM"
description: "Over the past few weeks, I’ve answered a bunch of questions that have asked something along the lines of “Should I use Hard Zoning or Soft Zoning?” And no, I have no idea why these questions are coming up now… The short answer If you’re familiar with FC Zoning as..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2012/01/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250910022545/https://brasstacksblog.typepad.com/brass-tacks/2012/01/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san.html"
pdf: "/brasstacks/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san.pdf"
comments:
  - author: "EMC Storage"
    date: "02/13/2012 at 11:35 PM"
    html: |-
      <p>I was delighted to find this web site.I wanted to thank you for your time reading this wonderful! I really enjoyed every bit of it and I&#39;ve marked to ensure that the blog post something new.<br />
      </p>
  - author: "ashwin"
    date: "02/27/2012 at 09:25 AM"
    html: |-
      <p>Absolutely class article. I have gone through lot of articles on the net, some of the them from vendors as well but this is so good. You have explained this concept so well. I will definitely recommend this article to everyone. Great job!</p>
  - author: "Erik Smith"
    date: "02/27/2012 at 10:23 AM"
    html: |-
      <p>Thanks Ashwin!</p>
  - author: "salvatore"
    date: "02/28/2012 at 04:06 PM"
    html: |-
      <p>Unbelievable that in this world, there is still someone able to explain simply and clearly complex stuff.</p>
      <p>Many thanks for that.</p>
  - author: "Erik Smith"
    date: "02/29/2012 at 07:41 PM"
    html: |-
      <p>Thanks Salvatore! I&#39;m glad to hear you found it useful and easy to read.</p>
      <p>Erik </p>
  - author: "Kevin Hughes"
    date: "03/12/2012 at 12:07 PM"
    html: |-
      <p>Nice job Erik! Couldn&#39;t have said it better myself (:-)</p>
  - author: "Erik Smith"
    date: "03/12/2012 at 06:46 PM"
    html: |-
      <p>Thanks Kevin!  Coming from one of the people who wrote the code that is responsible for the behavior described in this post, this is really nice feedback! </p>
      <p>Erik </p>
  - author: "Sreejith.c"
    date: "03/23/2012 at 08:08 AM"
    html: |-
      <p>Good Job Erik :)<br />
      This article is simple &amp; Informative .I have one request ...please share more articles like this .<br />
      </p>
  - author: "Jaspreet"
    date: "08/29/2012 at 10:10 PM"
    html: |-
      <p>Excellent Stuff Erik..!</p>
  - author: "Erik"
    date: "08/30/2012 at 09:40 AM"
    html: |-
      <p>Thanks Jaspreet!</p>
  - author: "saydur"
    date: "11/02/2012 at 04:40 PM"
    html: |-
      <p>Hi Erik,<br />
      I was searching for long for a clear explanation on soft vs hard zoning and believe me this is the best one I could find!!<br />
      Thanks a lot for this superb article!!</p>
      <p>Regards<br />
      Saydur</p>
  - author: "Erik"
    date: "11/09/2012 at 08:07 AM"
    html: |-
      <p>Hi Saydur, thanks!  Glad it was helpful and thanks for taking the time to comment.</p>
      <p>Erik </p>
  - author: "khursheed"
    date: "12/17/2012 at 09:37 PM"
    html: |-
      <p>Brilliant work Erik,Hats of to you...amazing understand and making it to simple for us to learn and deliver to the best of knowledge if you can throw some light on migration...on clariion to symmetrix or to vmax would be lot help ful and concepts of emc technology on san</p>
  - author: "Erik"
    date: "01/02/2013 at 04:03 PM"
    html: |-
      <p>Thanks Khursheed!  </p>
      <p>I&#39;ll see what I can do about a post on migration from one array to another.  Actually, I&#39;m working on a related topic for EMC World this year, so look for a post in the May timeframe.</p>
      <p>Erik </p>
  - author: "Deep"
    date: "06/20/2014 at 02:54 AM"
    html: |-
      <p>Best article for zoning</p>
  - author: "Rajesh sharma"
    date: "09/28/2016 at 01:37 PM"
    html: |-
      <p>most informative article I found on the web concerning SAN zoning.</p>
  - author: "catfancier42"
    date: "10/20/2022 at 03:25 PM"
    html: |-
      <p>10+ years later and the info here is still teaching old dogs old tricks, thereby proving that well researched and well written articles are timeless. Nice job Erik.</p>
---

<p>Over the past few weeks, I’ve answered a bunch of questions that have asked something along the lines of “Should I use Hard Zoning or Soft Zoning?”&#0160; And no, I have no idea why these questions are coming up now…&#0160; &#0160;&#0160;</p>
<p><strong>The short answer</strong></p>
<p>If you’re familiar with FC Zoning as well as the FC protocol and don’t require a detailed explanation, the short answer is; “<strong>You no longer have a choice.&#0160; As of today, all of the FC/FCoE switches supported by EMC provide hardware enforcement for both “WWPN” and “Domain, Port” based zones</strong>”.&#0160; For the sake of completeness, there are some situations where hardware enforcement is effectively disabled but as long as your <a href="http://www.emc.com/collateral/hardware/technical-documentation/h4331-networked-storage-cncpts-prtcls-sol-gde.pdf" target="_blank">fan-in and fan-out ratios</a> remain below 1:64 or 64:1 and/or you&#39;re not using NPIV, you won’t need to worry about this.&#0160;&#0160;</p>
<p>Read on if you’d like a bit more detail.</p>
<p><strong>The long answer...</strong></p>
<p>As I started writing this section it quickly became apparent that I would need to provide an introduction to zoning and this leads to a discussion about FC Login, discovery, etc.&#0160; So I’ll start with the basics first and then get a bit more detailed as I go.&#0160; To start with, let’s assume a configuration similar to the following.&#0160; &#0160;&#0160;</p>
<p><a href="/brasstacks/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san/6a013487ed263f970c0168e58a22af970c.jpg" style="display: inline;"><img alt="Zoning_one" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0168e58a22af970c image-full" src="/brasstacks/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san/6a013487ed263f970c0168e58a22af970c.jpg" title="Zoning_one" /></a></p>
<p>Starting from the left, the configuration consists of:</p>
<p>1)&#0160;&#0160;&#0160;&#0160;&#0160; A Host containing a single HBA/CNA port that has a WWPN (World Wide Port Name) of 10:00:00:00:00:00:00:00 and was assigned an FCID (Fibre Channel IDentifier) of 030100 during the Fabric login process.&#0160;&#0160;</p>
<p>2)&#0160;&#0160;&#0160;&#0160;&#0160; A FC Fabric containing two FC switches:</p>
<ul>
<li>FC/FCoE Switch Domain 3; and </li>
<li>FC/FCoE Switch Domain 4</li>
</ul>
<p>3)&#0160;&#0160;&#0160;&#0160;&#0160; A Storage array containing a port that has a WWPN of 50:00:09:71:20:30:40:50 and was assigned an FCID of 040200 during the Fabric login process.&#0160;&#0160;&#0160;</p>
<p>A&#0160;few points to take note of:</p>
<ul>
<li>This configuration could be all FC, all FCoE or a combination of both. </li>
<li>The HBA/CNA and Storage Array ports both have a WWPN that is assigned to the port in some vendor specific way AND an FCID that is assigned to each port by the switch during Fabric Login.</li>
<li>The middle byte of the FCIDs that I have shown correspond to the physical interface and this is not always the case (especially in Cisco environments)</li>
<li>I will only be talking about Open Systems hosts in this post.&#0160; Apologies to FICON users, you’ll have to wait for FC-SB-5 to be finished before any of this applies to you.</li>
</ul>
<p><strong>What is a zone, zone set, configuration, etc</strong></p>
<p>A zone is a collection of WWPNs, FCIDs or both that have been associated with one another for the purpose of allowing them to freely access one another.&#0160; Zones have to be added to a zone set or configuration and then activated onto a fabric in order for the access defined in the zone to become effective.&#0160; For example in the diagram below, I’ve updated the example topology so that it now shows a single zone named “TEST” that is a part of the Zone set/configuration “Test CFG” and contains two WWPN members.&#0160;</p>
<p><a href="/brasstacks/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san/6a013487ed263f970c0167608945e7970b.jpg" style="display: inline;"><img alt="Zoning_two" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0167608945e7970b image-full" src="/brasstacks/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san/6a013487ed263f970c0167608945e7970b.jpg" title="Zoning_two" /></a>&#0160;&#0160;</p>
<p>A couple of important points to note:</p>
<p>1)&#0160;&#0160;&#0160;&#0160;&#0160; For all practical purposes, the zone set “Test CFG” could have been activated on any switch in the Fabric.&#0160; This is because when a zone set is activated it is pushed to every switch in the fabric simultaneously.&#0160;</p>
<p>2)&#0160;&#0160;&#0160;&#0160;&#0160; As soon as the zone set has been activated, the zone members will be allowed to discover one another.&#0160; This is where the difference between hard zoning and soft zoning starts but before I dive into those details let’s talk about FC discovery first.</p>
<p><strong>The FC Discovery process</strong></p>
<p>&#0160;In order for an HBA/CNA or storage port to use a fabric, it has to login, perform registration and then perform discovery.&#0160; This process is illustrated in the following diagram and explained in more detail in the text that follows.</p>
<p><a href="/brasstacks/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san/6a013487ed263f970c016760894668970b.jpg" style="display: inline;"><img alt="Zoning_three" border="0" class="asset  asset-image at-xid-6a013487ed263f970c016760894668970b image-full" src="/brasstacks/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san/6a013487ed263f970c016760894668970b.jpg" title="Zoning_three" /></a></p>
<p>Each time an FC port initializes, it must perform some kind of login process in order for it to be able to use the fabric.&#0160; In practice each HBA/CNA uses a slightly different login process but they all have certain things in common.&#0160; One example is the need to transmit FLOGI (Fabric Login) and receive an ACC (accept) from the fabric before attempting to do anything else.&#0160; I point this out because although in practice all of the HBA/CNA or storage port implementations that I am familiar with will perform the same basic steps, the order of steps 5, 7 and 9 may be slightly different and the exact commands used within each step may vary as well.</p>
<p><span style="text-decoration: underline;">Step 0 (Not shown in diagram)</span></p>
<p>Assuming a port is initializing from the power off or loss of signal/sync state, speed negotiation and Link Initialization will be performed.&#0160; At the end of the Link Initialization process, the HBA/CNA or Storage port that is initializing will just be passing IDLE frames back and forth with the switch port it has been connected to and both ports will be considered to be in the ACTIVE state.</p>
<p><span style="text-decoration: underline;">Step 1 (FLOGI) </span></p>
<p>FLOGI (Fabric Login) is the first frame transmitted by an end device that is attempting to attach to a switch.&#0160; The FLOGI contains many bits of information about this initializing end device (N_Port), but for the sake of the discussion on zoning, we only need to recognize that the initializing N_Port’s WWPN (World Wide Port Name) is included in the FLOGI.&#0160; As shown previously, this WWPN can be used in a zone to allow the initializing N_Port to access another N_Port.</p>
<p><span style="text-decoration: underline;">Step 2 (FLOGI ACC)</span></p>
<p>Assuming the switch is functioning properly, is not too busy and there are no configuration parameters set on the switch that would prevent a particular N_Port from logging in, the switch will respond to the FLOGI with an FLOGI ACC.&#0160; The format of the FLOGI ACC is identical to the FLOGI request but the information contained within it will be specific to the responding switch/switch port.&#0160; Also, a VERY IMPORTANT piece of information that is relevant to zoning enforcement known as the FCID (Fibre Channel IDentifier) is provided to the N_Port in the FLOGI ACC. &#0160;Unlike the WWPN, this FCID will be present in every frame that will be transmitted by the N_Port and as you will see, the FCID effectively becomes the N_Port’s identity while logged into the fabric.&#0160; The relationship a WWPN has with the FCID it has been assigned by the fabric is one of the factors that allows for zoning to be enforced in hardware.</p>
<p><span style="text-decoration: underline;">Step 3 (PLOGI NS)</span></p>
<p>One the FLOGI has been accepted by the switch, the N_Port will login with the Name Server.&#0160; Again, this has to be done in order for the N_Port to be able to register with and send queries to the Name Server.</p>
<p><span style="text-decoration: underline;">Step 4 (PLOGI ACC)</span></p>
<p>&#0160;Assuming the switch is functioning properly and is not too busy, it will respond to the PLOGI with PLOGI ACC.&#0160; The format of the PLOGI ACC is identical to the PLOGI request but the information contained within it will be specific to the responding switch/switch port.</p>
<p><span style="text-decoration: underline;">Step 5 (Register with the Name Server)</span><strong></strong></p>
<p>Once the attaching N_Port is logged into the Name Server it may register with it.&#0160; There are many different registration commands that an N_Port could use but a typical one is RFT_ID or in plain English “Register the specified FC-4 Type for the provided FCID”.&#0160; In this case we will assume that all N_Ports involved either have or will register an FC-4 Type of “SCSI-FCP”.&#0160; Note, although it’s a bit out of scope for this post, I will mention that this isn’t usually the case.&#0160; Many N_Ports (especially targets) choose to register with the Name Server in multiple ways, the purpose for doing so is to ensure that no matter what Name Server query an initiator uses, the target will always be discoverable.&#0160;&#0160;</p>
<p><span style="text-decoration: underline;">Step 6 (Name Server Accepts registrations)</span><strong></strong></p>
<p>&#0160;Assuming the switch is functioning properly and is not too busy, it will accept the registrations.&#0160; If this fails, an attaching N_Port should retry.</p>
<p><span style="text-decoration: underline;">Step 7 (SCR - State Change Registration)</span><strong></strong></p>
<p>The attaching N_Port will perform a full registration for RSCNs.&#0160; By doing so, the N_Port is requesting the switch to send it a Registered State Change Notification (RSCN) every time something in the fabric changes.&#0160; These changes currently include events like the addition and removal of a Domain (e.g., switch) as well as a <span style="text-decoration: underline;">zoning change being made to the fabric that impacts the device</span>.</p>
<p><span style="text-decoration: underline;">Step 8 (Fabric Controller accepts the State Change Registration)</span><strong></strong></p>
<p>Assuming the switch is functioning properly and is not too busy, it will accept the SCR</p>
<p><span style="text-decoration: underline;">Step 9 (Query the Name Server)</span><strong></strong></p>
<p>At this point in the login process the attaching N_Port will query the Name Server in an attempt to discover what other devices are logged into the fabric and available for it to communicate with.&#0160; Since I stated that we would assume all N_Ports in the fabric would register an FC-4 type of SCSI-FCP (see step 5), we’ll assume that the attaching N_Port will use a Name Server query called GID_FT or in plain English “Get Port Identifiers for the devices that registered the specified FC-4 type” and will specify an FC-4 of SCSI-FCP.</p>
<p><strong>And finally … information directly relevant to the topic of Hard Zoning versus soft zoning.</strong></p>
<p><span style="text-decoration: underline;">Step 10 (Name Server response to queries)</span></p>
<p>In response to the Name Server query, the switch will return a list of port identifiers (i.e., 030100 and 040200).&#0160; More specifically, the switch will only return the Port IDs for other FC devices that:</p>
<ol>
<li>have registered an FC-4 of SCSI-FCP (since that is what we queried for); AND </li>
<li>share a common zone with the device that queried the Name Server.&#0160; </li>
</ol>
<p>For example, in the following diagram Host 1, Storage 1A and Storage 1B are all in the same Zone.&#0160; If any of these devices were to query the Name Server, they should only get 3 Port IDs back.&#0160; <strong>In the case of a switch that only supports “soft zoning”; zoning is enforced by allowing N_Ports to discover only those Port IDs that are associated with N_Ports that they have been granted access to (via zoning).&#0160; Port IDs associated with N_Ports that do not share a common zone with the querying N_Port will not be returned in Name Server responses. &#0160;</strong>&#0160;&#0160;</p>
<p>The downside of soft zoning is the switch does nothing to prevent a rogue host from transmitting frames directly to another N_Port’s Port ID.&#0160; To some this represents a serious security flaw and it’s hard to argue against this point.&#0160; However, in practice, this behavior is more of a problem when you had a malfunctioning adapter or an incorrectly programmed driver that would insist on communicating with another device even if access to that device was removed via a zoning change.&#0160;&#0160;</p>
<p><a href="/brasstacks/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san/6a013487ed263f970c016760894748970b.jpg" style="display: inline;"><img alt="Zoning_four" border="0" class="asset  asset-image at-xid-6a013487ed263f970c016760894748970b image-full" src="/brasstacks/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san/6a013487ed263f970c016760894748970b.jpg" title="Zoning_four" /></a><br /><span style="text-decoration: underline;">Step 11+ (End to End PLOGI) see diagram below </span></p>
<p>Once an N_Port discovers the other port IDs it can communicate with, it will perform an end to end PLOGI with them.&#0160; In practice only Hosts (Initiators) end up performing this PLOGI and they are usually smart enough to not PLOGI themselves.</p>
<p>When the initiator transmits the PLOGI, it will set the D_ID (Destination ID ) of the frame to be equal to one of the Port IDs returned from the Name Server and it will set the S_ID (Source ID) of the frame to be equal to its own Port ID (assigned in FLOGI ACC).&#0160;</p>
<p>When the switch receives the end to end PLOGI, if it supports Hard zoning, it will check the D_ID of the frame and make sure that the specified S_ID is allowed to access (is zoned to have access) the specified D_ID.&#0160; If yes, the PLOGI is forwarded on to the destination if not, the PLOGI is dropped.&#0160; This is what is commonly referred to as Hard Zoning or Hardware enforced zoning.&#0160;&#0160; Since the PLOGI is dropped, the login process never continues past this point.&#0160; I’ve heard but have not been able to confirm in the lab that some switch vendors implement hard zoning by trapping all PLOGIs from N_Ports at the fabric ingress port and forwarding them to the control plane of the switch.&#0160; The control plane then only forwards those PLOGI frames that should be allowed.&#0160; &#0160;&#0160;&#0160;&#0160;</p>
<p><a href="/brasstacks/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san/6a013487ed263f970c016760894818970b.jpg" style="display: inline;"><img alt="Zoning_five" border="0" class="asset  asset-image at-xid-6a013487ed263f970c016760894818970b image-full" src="/brasstacks/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san/6a013487ed263f970c016760894818970b.jpg" title="Zoning_five" /></a></p>
<p><strong>Additional considerations</strong></p>
<p>There is so much more that could be said on the topic of hardware enforced zoning.&#0160; One point that I should mention is that not all switches supported by EMC today enforce zoning at the fabric ingress port.&#0160; In fact, some of the earlier Brocade products would enforce at the fabric egress port.&#0160;&#0160; The net result was, for all practical purposes, the same as if the frame was dropped at the ingress but if I didn’t mention it someone else would have…</p>
<p>Thanks for reading!</p>
