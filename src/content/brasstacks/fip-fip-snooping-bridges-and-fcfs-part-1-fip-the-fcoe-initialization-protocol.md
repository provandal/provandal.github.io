---
title: "FIP, FIP Snooping Bridges, and FCFs (Part 1 – “FIP”, the FCoE Initialization Protocol)"
pubDate: 2010-11-09
postedAt: "04:44 AM"
description: "Background: I had an interesting conversation the other day with a colleague in another engineering group at EMC. He was in the process of getting ready to order a 10 GbE switch to support some NAS testing. He also mentioned that he would eventually like to test FCoE. Although I..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2010/11/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250913032629/https://brasstacksblog.typepad.com/brass-tacks/2010/11/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol.html"
pdf: "/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol.pdf"
comments:
  - author: "Ivan Pepelnjak"
    date: "11/30/2010 at 06:38 AM"
    html: |-
      <p>Erik,</p>
      <p>This is a fantastic introduction to FCoE login processing. However, the basic question remains: why would you mandate that a DCB-enabled bridge supports FIP snooping? </p>
      <p>FIP snooping is a nice security feature, but it&#39;s not mandatory to make FCoE work ... and you should always put FCoE traffic in a separate VLAN anyway.</p>
      <p>Looking forward to future posts!<br />
      Ivan</p>
  - author: "Erik Smith"
    date: "11/30/2010 at 07:02 AM"
    html: |-
      <p>Hi Ivan, thanks!  My next post should be ready in a day or so and it will explain exactly why I think FIP Snooping is required.  </p>
      <p>Erik   </p>
  - author: "Streif Vest"
    date: "12/27/2010 at 06:22 AM"
    html: |-
      <p>Thank you, Erik, for the topic. I read FC-BB-6 at this moment (FCoE) and try to understand FIP procedures. I think that you describe basic routine very well.</p>
  - author: "Mohan"
    date: "03/03/2012 at 10:30 AM"
    html: |-
      <p>Excellent write up on FIP. Thanks very much.<br />
      Just one question, why there must be a VLAN associated with every VSAN? Just I could not understand this? regards. Mohan</p>
  - author: "Erik Smith"
    date: "03/04/2012 at 08:17 AM"
    html: |-
      <p>Hi Mohan, thanks!  </p>
      <p>In regards to your question, there can only be one VSAN per VLAN due to a requirement in the FCoE standard (FC-BB-5).  Essentially, if you have more than one VSAN per VLAN, it would be possible to have duplicate FPMAs (Fabric Provided MAC Addresses) and this can lead to data corruption under the right circumstances.</p>
---

<p><strong>Background:</strong></p>
<p>I had an interesting conversation the other day with a colleague in another engineering group at EMC.&#0160; He was in the process of getting ready to order a 10 GbE switch to support some NAS testing.&#0160; He also mentioned that he would eventually like to test FCoE.&#0160; Although I won’t mention it by name, the switch he was considering (mainly due to its low cost) was going to be problematic since it didn’t support FIP Snooping.&#0160; When I pointed this out he responded that the product’s literature stated it supported FCoE and the vendor had apparently received an industry award for this.&#0160; My response was something along the lines of:&#0160;</p>
<p><strong>They can claim whatever they want :-)&#0160; However, unless they implement FIP Snooping, E-Lab would not qualify or support it. </strong></p>
<p><strong>To provide a bit more detail, currently there are two different types of &quot;FCoE-capable&quot; switches: &#0160;FIP Snooping Bridges (FSBs) and Fibre Channel Forwarders (FCFs).&#0160; </strong></p>
<p><strong>An FSB makes use of DCBX, PFC, ETS, and Dynamic ACLs (as defined in FC-BB-5).&#0160; The last requirement, Dynamic ACLs, implies that the device must be FIP Aware (a.k.a., FIP Snooping).&#0160; Currently, an FSB must connect to an FCF in order for FCoE to function.&#0160; This is due to the fact that there is no support for the PT2PT or VN2VN protocols, both of which are FC-BB-6 features, in any of the ENodes are available today.</strong></p>
<p><strong>An FCF is an FSB that also provides FC Services (Name Server, Fabric Server, etc.) as well as FC/FCoE encapsulation and de-encapsulation.&#0160; FCFs have to be compliant with FC-BB-5, FC-SW, FC-GS, FC-LS, FC-FS, etc.&#0160; Because of these requirements, only Brocade, Cisco, and QLogic provide FCFs today.</strong></p>
<p><strong>Finally, since FSBs must be connected to an FCF to support FCoE, you are also going to have to buy an FCF to support your FCoE testing which may negate the cost savings you are trying to achieve.&#0160; In addition, if you want to use an FSB, you will have to use a Cisco FCF, since currently Brocade FCFs will not work with FIP Snooping Bridges.&#0160; This is mainly due to the fact that Brocade only supports a single FCoE login per physical interface.</strong>&#0160;</p>
<p>After I responded, I got the sinking feeling that I am going to be answering this question multiple times if 10 GbE switch vendors all start claiming support for FCoE.&#0160; So, I decided to create a post on FIP, FIP Snooping, and FCFs.&#0160; Ideally, I’d like to arm you with enough information to make an informed decision about a vendor’s claim of FCoE support.&#0160; As I started writing it, I quickly realized that I’m going to have to create multiple installments due to the amount of information I am going to have to cover.&#0160; This particular installment discusses the FCoE Initialization Protocol, or “FIP”.&#0160; I decided to start with FIP because you need to understand what it is and how it works to appreciate the difference between a 10 GbE switch, an FSB, and an FCF.&#0160;</p>
<p><strong>FIP, the FCoE Initialization Protocol – Why is it needed?</strong></p>
<p>Before I describe what FIP is and how it works, it would probably help if I described why it’s needed.&#0160; To do this, it’s important to back up and look at some of the network features that the Fibre Channel Protocol relies on to function properly.</p>
<ol>
<li>Fibre Channel relies on the fact that there is a physical link between the two ports being attached.</li>
<li>Due to the use of Well Known Addresses, FC N_Ports know which address to log in with.</li>
<li>FC assumes a point-to-point connection exists between an N_Port and the fabric being logged into.&#0160; (BTW, notice I said N_Port not NL_Port…)</li>
<li>Devices are implicitly logged out from the fabric should the physical link be lost between an N_Port and the switch it connects to.&#0160; This is an extremely important point because this allows for things like RSCNs to be generated and for the distributed Name Server to be kept in sync.</li>
<li>Due to the point-to-point nature of FC, there is implicit security since a man-in-the-middle attack is very difficult to accomplish in this topology.</li>
</ol>
<p>When you start to think about running FC over Ethernet without FIP, the potential topologies that could result would violate some of the expectations of the FC protocol.&#0160; With Ethernet:&#0160;</p>
<ul>
<li>There is not necessarily a single physical link between an ENode and its FCF; as a result there is not always an implicit logout when a physical link is lost, which negatively impacts RSCN generation as well as the distributed name server.&#0160;</li>
<li>ENodes do not know the address of the FCF that will allow login, or if one even exists in the network.</li>
<li>There is no one-to-one relationship between an ENode and a fabric, but as I will describe later on, this could be a good thing.</li>
<li>There is no implicit security so a man-in-the-middle attack is theoretically possible.</li>
</ul>
<p>So, you may be asking how all of this relates to FIP.&#0160; The answer is: <strong>FIP bridges the gap between the expectations of the FC protocol and the reality of an FCoE topology</strong>.</p>
<p>FIP does this by:</p>
<ul>
<li>Allowing ENodes to discover who to log in with.</li>
<li>Enabling a single ENode to communicate with multiple different FC fabrics and as a result a one-to-many relationship is built in.&#0160; For me, this is one of the more exciting use cases for FCoE.&#0160; I mean, imagine being able to log in to multiple FC fabrics with a single HBA and not have to use some form of Layer 3 FC Routing such as IVR, FCR or IR!</li>
<li>Including Link Keep Alive and Clear Virtual Link functions to allow a loss of a physical link or logical connectivity to be detected and for both ends of the virtual link to be notified when this happens.&#0160; This allows RSCN to function properly and for the distributed name server to remain in sync.</li>
<li>Reducing the security concerns with FCoE provided that FIP snooping and dynamic ACLs are implemented.&#0160;&#0160;&#0160;&#0160;</li>
</ul>
<p><strong>FIP, the FCoE Initialization Protocol – How does it work?</strong></p>
<p>To describe how the FCoE Initialization Protocol (FIP) works, the following topology diagram will be used.</p>
<p><a href="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/6a013487ed263f970c013488d00a43970c.jpg" style="display: inline;"><img alt="Topo" border="0" class="asset  asset-image at-xid-6a013487ed263f970c013488d00a43970c image-full" src="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/6a013487ed263f970c013488d00a43970c.jpg" title="Topo" /></a>&#0160;</p>
<p>The diagram consists of a DCB Cloud containing a single DCB-capable Lossless Ethernet switch.&#0160; Attached to the Lossless Ethernet switch is a Converged Network Adapter (CNA) as well as two Fibre Channel Forwarders (FCFs).&#0160; The FCFs are then connected to a single FC fabric.&#0160; A couple of important points to note are: the CNA has three MAC Addresses.&#0160; As shown in the diagram, they are the Universal, ENode, and VN_Port MAC Addresses.&#0160; The Universal MAC is used for non-FCoE traffic, IP, etc.&#0160; As you will see, the ENode MAC is used in the FCoE Initialization Protocol and the VN_Port MAC is assigned by the fabric to the CNA and is used for FCoE frames.&#0160; Other &#0160;important points are each FCF has been assigned a priority and finally that the fabric has a WWNN associated with it and this is typically the WWN of the principal switch in the FC fabric.&#0160; Again, more on how these are used later.</p>
<p>Before diving into the details of how FIP works, keep in mind that FIP allows an ENode to:</p>
<ul>
<li>Perform VLAN and FCF discovery</li>
<li>Ensure that the Layer 2 network is capable of supporting mini-jumbo frames </li>
<li>Perform fabric login</li>
<li>Use LKA (Link Keep Alive) to maintain the virtual link with the FCF</li>
</ul>
<p>All of these were identified previously as important things to do when trying to run the FC protocol over an Ethernet topology.&#0160;</p>
<p><span style="text-decoration: underline;">FIP VLAN Request</span></p>
<p>Once DCBX information has been exchanged, the CNA will transmit a FIP VLAN Request in order to determine which VLAN provides support for FCoE.</p>
<p><a href="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/6a013487ed263f970c0133f5b3b605970b.jpg" style="display: inline;"><img alt="FIPVLANRequest" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0133f5b3b605970b image-full" src="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/6a013487ed263f970c0133f5b3b605970b.jpg" title="FIPVLANRequest" /></a>&#0160;</p>
<p>The FIP VLAN Request is multicast to the destination MAC Address of ALL-FCF-MACs.&#0160; The Source Address for the VLAN Request is the ENode MAC and it is important to note that the frame is transmitted without an 802.1Q (VLAN) tag.&#0160; As a result, the VLAN Request will use the default VLAN for the switch port that it is being attached to.&#0160; Another important point to note is that earlier in this post I mentioned the concept of Dynamic ACLs.&#0160; In order for Dynamic ACL updates to work properly, these FIP VLAN Requests must be allowed on a switch port by default.</p>
<p>&#0160;</p>
<p><span style="text-decoration: underline;">FIP VLAN Notification</span></p>
<p>Since the VLAN Request was multicast, any device listening for frames destined to ALL-FCF-MACs, such as an FCF, may transmit a FIP VLAN Notification to the ENode MAC.</p>
<p><a href="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/6a013487ed263f970c013488d3b4f7970c.jpg" style="display: inline;"><img alt="FIPVLANNotification" border="0" class="asset  asset-image at-xid-6a013487ed263f970c013488d3b4f7970c image-full" src="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/6a013487ed263f970c013488d3b4f7970c.jpg" title="FIPVLANNotification" /></a>&#0160;</p>
<p>A couple of important points to note are the number of notifications that an ENode can receive will be equivalent to the number of FCFs listening on the default VLAN.&#0160; This will include FCFs that are providing FCoE services on different VLANs, so the ENode can get Notifications for multiple FCoE VLANs.&#0160; The ENode determines the VLAN by examining the value in the FCoE VID field.&#0160; Finally, the notification will include the FCFs MAC Address, which will be used for subsequent FIP Frames.</p>
<p>&#0160;</p>
<p><span style="text-decoration: underline;">FIP Discovery Solicitation</span></p>
<p>Once the ENode has discovered which FCFs exist, it needs to determine which ones it can log in with.&#0160; It does this by transmitting a multicast Solicitation to ALL-FCF-MACs.&#0160;</p>
<p><a href="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/6a013487ed263f970c013488d3b69d970c.jpg" style="display: inline;"><img alt="FIPSolicitation" border="0" class="asset  asset-image at-xid-6a013487ed263f970c013488d3b69d970c image-full" src="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/6a013487ed263f970c013488d3b69d970c.jpg" title="FIPSolicitation" /></a>&#0160;</p>
<p>Notice that the Solicitation is tagged with a VLAN ID.&#0160; If FCoE is being supported on multiple VLANs, there would be multiple Solicitations, one sent to each VLAN where FCoE is being supported.&#0160; Another important piece of information contained in the solicitation is the MAX_FCOE_SIZE value.&#0160; This value will be used by the FCF in the response to the Solicitation.</p>
<p><span style="text-decoration: underline;">FIP Discovery Advertisement</span></p>
<p>In response to the Solicitation, each FCF will respond with a unicast FIP Advertisement that will contain:</p>
<ul>
<li>The priority of the FCF.&#0160; This is used by the Enode to help determine which FCF should be logged into if there are multiple FCFs connected to the same fabric.</li>
<li>The name of the fabric the FCF is attached to. This allows the ENode to determine if two FCFs are attached to the same fabric.</li>
<li>In addition, a pad field that inflates the Advertisement to be the size of a full FCoE Frame.&#0160; The purpose of the pad field is to validate that the path between the FCF and the ENode is capable of transporting FCoE frames that are the maximum size supported by the ENode.</li>
</ul>
<p><a href="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/6a013487ed263f970c0133f5b3bc8f970b.jpg" style="display: inline;"><img alt="FIPDiscoveryAdvertisement" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0133f5b3bc8f970b image-full" src="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/6a013487ed263f970c0133f5b3bc8f970b.jpg" title="FIPDiscoveryAdvertisement" /></a>&#0160;<br />&#0160;</p>
<p>Another function of the Advertisement is to act as a catalyst for updating the dynamic ACL.&#0160; The reception of this frame would cause FCoE frames to be allowed to be sent from this ENode to the DA of the responding FCFs.</p>
<p><span style="text-decoration: underline;">&#0160;</span></p>
<p><span style="text-decoration: underline;">FIP Virtual Link Instantiation Request (FLOGI)</span></p>
<p>As the Advertisements are received from the FCFs, the CNA will store them in an “Internal FCF list” and then select one from that list to perform fabric login with.&#0160; In this example, the CNA will log in to the FCF with the lower priority.</p>
<p><span style="font-family: &#39;Times New Roman&#39;; font-size: 12pt; mso-fareast-font-family: &#39;Times New Roman&#39;; mso-ansi-language: EN-US; mso-fareast-language: EN-US; mso-bidi-language: AR-SA;"><span style="font-family: &#39;Times New Roman&#39;; font-size: 12pt; mso-fareast-font-family: &#39;Times New Roman&#39;; mso-ansi-language: EN-US; mso-fareast-language: EN-US; mso-bidi-language: AR-SA;"><span style="font-family: &#39;Times New Roman&#39;; font-size: 12pt; mso-fareast-font-family: &#39;Times New Roman&#39;; mso-ansi-language: EN-US; mso-fareast-language: EN-US; mso-bidi-language: AR-SA;">
<p class="MsoNormal" style="margin: 0pt;"><a href="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/6a013487ed263f970c013488d3bafe970c.jpg" style="display: inline;"><img alt="FIPFLOGI" border="0" class="asset  asset-image at-xid-6a013487ed263f970c013488d3bafe970c image-full" src="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/6a013487ed263f970c013488d3bafe970c.jpg" title="FIPFLOGI" /></a>&#0160;</p>
</span></span></span></p>
<p class="MsoNormal" style="margin: 0pt;"><span style="font-family: %value; text-decoration: underline;"><span style="font-size: small;">FIP Virtual Link Instantiation Response (FLOGI ACC)</span></span></p>
<p><span style="font-family: %value; font-size: 12pt; mso-fareast-font-family: &#39;Times New Roman&#39;; mso-ansi-language: EN-US; mso-fareast-language: EN-US; mso-bidi-language: AR-SA;">Finally, the FCF will respond to the Fabric Login with a Fabric Login accept.<span style="mso-spacerun: yes;">&#0160; </span>This is the step where the CNA is provided with its FPMA and it will start to use actual FCoE frames to complete the rest of the login process. </span></p>
<p><span style="font-family: &quot;Times New Roman&quot;; font-size: 12pt; mso-fareast-font-family: &#39;Times New Roman&#39;; mso-ansi-language: EN-US; mso-fareast-language: EN-US; mso-bidi-language: AR-SA;"><a href="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/6a013487ed263f970c0133f5b3c063970b.jpg" style="display: inline;"><img alt="FIPFLOGIACC" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0133f5b3c063970b image-full" src="/brasstacks/fip-fip-snooping-bridges-and-fcfs-part-1-fip-the-fcoe-initialization-protocol/6a013487ed263f970c0133f5b3c063970b.jpg" title="FIPFLOGIACC" /></a>&#0160;<br /></span></p>
<p>Once the FIP FLOGI ACC has been received, the ENode will continue the login process by transmitting a PLOGI to the Name Server.&#0160; This PLOGI is encapsulated in an FCoE frame, not a FIP Frame.&#0160;&#0160;</p>
<p class="MsoNormal" style="margin: 0pt;"><span style="font-family: Times New Roman; font-size: small;">&#0160;</span></p>
<p class="MsoNormal" style="margin: 0pt;"><span style="font-family: %value; font-size: small;">Well, it still ended up being a long post but I hope you have a better understanding of why FIP is needed and how it works.<span style="mso-spacerun: yes;">&#0160; </span>In part two, I will focus on the differences between 10 GbE switches, FSBs, and FCFs. </span></p>
<p class="MsoNormal" style="margin: 0pt;"><span style="font-family: Times New Roman; font-size: small;">&#0160;</span></p>
<p class="MsoNormal" style="margin: 0pt;"><span style="font-family: %value; font-size: small;">Thanks for reading!</span></p>
<p><span style="font-family: %value; font-size: 12pt; mso-fareast-font-family: &#39;Times New Roman&#39;; mso-ansi-language: EN-US; mso-fareast-language: EN-US; mso-bidi-language: AR-SA;">Erik</span></p>
<p><span style="font-family: &quot;Times New Roman&quot;; font-size: 12pt; mso-fareast-font-family: &#39;Times New Roman&#39;; mso-ansi-language: EN-US; mso-fareast-language: EN-US; mso-bidi-language: AR-SA;">&#0160;</span></p>
