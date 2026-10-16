---
title: "FC and FCoE versus iSCSI – “Network-centric” versus “End-Node-centric” provisioning"
pubDate: 2012-02-13
postedAt: "09:25 PM"
description: "Which is easier to use: FC, FCoE, or iSCSI? This is the question we wanted to answer as we set out few months ago to test a series of nine configurations in the lab. Our approach was to determine the number of provisioning steps required when using each protocol to..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2012/02/fc-and-fcoe-versus-iscsi-network-centric-versus-end-node-centric-provisioning.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250911105306/https://brasstacksblog.typepad.com/brass-tacks/2012/02/fc-and-fcoe-versus-iscsi-network-centric-versus-end-node-centric-provisioning.html"
pdf: "/brasstacks/fc-and-fcoe-versus-iscsi-network-centric-versus-end-node-centric-provisioning/fc-and-fcoe-versus-iscsi-network-centric-versus-end-node-centric-provisioning.pdf"
comments:
  - author: "Etherealmind"
    date: "02/14/2012 at 05:12 PM"
    html: |-
      <p>Two about things about iSCSI that might be worth considering. </p>
      <p>1. Many more people understand TCP/IP, or think they do, than FibreChannel. FibreChannel is a complex technology to learn and be confident about when compared to a technology you use everyday. </p>
      <p>2. The storage industry originally embraced iSCSI, only to turn to FC and have been acting like snobs about iSCSI ever since. It&#39;s hard to have a rational discussion about FC over provisioning, unnecessary costs, and pointless over specification. </p>
      <p>When you point out that iSCSI has many steps it sort of fails to calculate many of the complexities that went into establishing the FC network. Whereas an Ethernet network is much simpler to build and use, and costs less than an FC network. </p>
      <p>But, nice article. Does highlight some of the advantages of FC especially for more certain applications where simplicity is important for less errors on the configuration side. </p>
  - author: "Erik Smith"
    date: "02/15/2012 at 08:09 AM"
    html: |-
      <p>Hi Greg, thanks for the comment!  I agree with your point about the perceived complexity of FC / simplicity of Ethernet.  This is one of the reasons that I&#39;ve been pushing TDZ.</p>
      <p>In regards to your second point, I&#39;d place myself firmly in the &quot;recovering FC snob&quot; category of users...  I think my prejudice against iSCSI was due mainly to:<br />
      1. Customer adoption rates,<br />
      2. the bandwidth constraints of 1GbE; and <br />
      3. the lack of iSCSI management tools.<br />
      However, since:<br />
      1. customers are now voting with their pocketbooks in favor of iSCSI, <br />
      2. 10GbE is available (if required by the application); and <br />
      3. the environments that are using iSCSI don&#39;t need the same class of management tools as customers managing larger FC SANs.</p>
      <p>clearly I needed to revisit my bias or fall out of touch with reality…</p>
      <p>Besides, unless someone defines how to use DCB in an SDN environment, iSCSI is clearly going to be the only choice when there’s a need to perform block I/O in these environments.   </p>
      <p>Regards, Erik <br />
      </p>
  - author: "Anton Kolomyeytsev"
    date: "02/17/2012 at 07:31 AM"
    html: |-
      <p>&quot;if you require a separate high performance (up to 16GB/s) and fault tolerate SAN, then choose FC or FCoE&quot;</p>
      <p>Sorry but this is simply not true... You can easily build iSCSI SAN using MPIO and 10 GbE connections (as many as you wish). Resulting solution would run circles around any FC SAN implementation @ fraction of cost. You may wish to study NetApp and VMware FS Vs. iSCSI results like the one provided below:</p>
      <p><a href="https://communities.netapp.com/community/netapp-blogs/virtualstorageguy/blog/2010/01/06/new-vmware-and-netapp-protocol-performance-report" rel="nofollow">https://communities.netapp.com/community/netapp-blogs/virtualstorageguy/blog/2010/01/06/new-vmware-and-netapp-protocol-performance-report</a></p>
      <p>Good luck!</p>
      <p>Anton</p>
      <p>StarWind Software </p>
  - author: "Erik Smith"
    date: "02/17/2012 at 08:45 AM"
    html: |-
      <p>Anton, thanks for taking the time to comment, but I disagree.  Your assertion of &quot;..Resulting solution would run circles around any FC SAN implementation @ fraction of cost.&quot;, has a few problems:</p>
      <p>1. I specifically mentioned 16Gb/s FC, can you explain how 10GbE is going to run circles around 16G FC?<br />
      2. FC has no overhead from TCP.  While this adds a non-trivial requirement to the network (i.e., must be lossless), the end result to the host is more CPU cycles available for doing real work.  I agree that modern CPUs have sufficient capacity to do the extra TCP related work and so achieving line rate transfer with TCP based protocols is not a problem.  But they are not the same and FC comes out looking slightly better here.  The point is I believe most &quot;real world&quot; performance measurements that compare FC/FCoE and TCP based protocols will show that there&#39;s practically very little difference between them today..  <br />
      3. In regards to cost, I specifically said &quot;if you require a separate high performance (up to 16GB/s) and fault tolerate SAN&quot;.  The two key pieces of information that you need to re-consider are &quot;Separate&quot; and &quot;Fault Tolerant&quot;.  For those environments that require these attributes, there would be no cost savings since the networking components are, by definition, separate.  In addition Fault Tolerant indicates that you&#39;ll have at least two of these separate networks and they&#39;ll most likely be constructed from &quot;Director Class products&quot;.  With these requirements in mind, how are you proposing to provide an iSCSI solution at a (significant) fraction of the cost.</p>
      <p>Regards, Erik</p>
  - author: "Stuart"
    date: "02/17/2012 at 04:35 PM"
    html: |-
      <p>Interesting article, the FC set up seems a little over simplified, but its still my clear favourite. I have always found iscsi quite simplistic as being ip based no understanding of fabrics is required. Interesting comments around 10Gb networking! Was there any testing around vmw and NFS? </p>
  - author: "Erik Smith"
    date: "02/17/2012 at 05:36 PM"
    html: |-
      <p>Hi Stuart, thanks!  In regards to FC, did I miss any configuration steps?</p>
      <p>Regards, Erik </p>
  - author: "The_socialist"
    date: "02/29/2012 at 07:04 PM"
    html: |-
      <p><br />
      This is REALLY good.</p>
      <p>I mean I&#39;m sure each group would pick on little things. </p>
      <p>If I had to pick on something, I would pick on the lack of NFS (which others already did =)</p>
      <p>but overall the two ideas:</p>
      <p>1.) Look at each protocol from a &quot;how many physical &quot;things&quot; from start to finish to get it working.</p>
      <p>2.) Network Centric vs Node Centric</p>
      <p>Are REALLY good items to cover and very interesting topics.</p>
      <p>I also think item #2 begs for another look from a different angle. </p>
      <p>How much time is really spent on the CNA/HCA/HBA-&gt;TOR/EOR&amp;||Director vs how much time is spent managing the storage targets themselves. </p>
      <p>I think you are on to something here. I really more analysis is needed on &quot;care &amp; feeding&quot; and then a look at how much impact that really has on buying/usage decisions.  </p>
      <p>Again, nice work guys. </p>
  - author: "Erik Smith"
    date: "02/29/2012 at 08:09 PM"
    html: |-
      <p>Thanks Jon, I appreciate the feedback.</p>
      <p>The post was intended to compare the provisioning steps for block I/O protocols and as a result NAS wasn&#39;t considered.  </p>
      <p>In addition, I&#39;ve only started REALLY learning about NAS in the past few weeks.  Putting aside the multipathing, performance and security considerations for a moment, I&#39;ll say that I&#39;ve spent some time in the lab working with NAS over the past week or so and I really like it.  I was able to configure an NFS server and 4 clients in less than an hour and I started the process without having a clue.  </p>
      <p>I&#39;m not sure I&#39;ll revist the topic because I still don&#39;t feel a file to block provisioning comparison makes sense in the general (non-VMware) case. </p>
      <p>The CNA/HBA and Network provisioning steps were all that were required in my topology, but your point about more complex topologies requiring additional work is a good one.</p>
      <p>Erik </p>
  - author: "The_socialist"
    date: "03/01/2012 at 05:28 AM"
    html: |-
      <p>I figured as much on the NFS, I was just looking for something to pick on. </p>
      <p>I wasn&#39;t clear, I didn&#39;t mean complexity due to topology. </p>
      <p>I meant that when I was a SAN Admin I found that I spend VERY little time dealing with hbas/switches/directors. The majority of my time was spent managing the arrays. Symms and Lightnings took most of my time. Managing, upgrading, building luns, optimization, replication, backups etc. </p>
      <p>As so for me I found that adding NFS or iSCSI access to my arrays didn&#39;t really change my job much. Just meant more customers were using my storage. </p>
      <p>And in some ways the ethernet based access was easier. For the FC stuff I was on task all the way down to the HBA. For NFS, I got to send the pissed off user to the Network team =)</p>
  - author: "Chris Greer"
    date: "03/14/2012 at 09:21 PM"
    html: |-
      <p>Good article.  I&#39;m not sure it is an apples to apples configuration.  For example, you have VSANs in FCoE but your FC example assumes no VSANS.  If you are using VSANS, you have some additional steps in FC of configuring VSAN membership for ports.<br />
      Also I would argue you probably should be creating 2 separate zones in 2 different zonesets (assuming you have separate fabrics).</p>
      <p>Also, any modern Linux variant and Windows 2008 have the iscsi initiator built-in, so that cuts off like 3 steps in Windows and Linux.  Even so, you mention that the install guide for HBA/CNA is a 50 page document so maybe that should be in bold.</p>
      <p>Having used all three, I personally think iSCSI is a lot less complex operationally.  You eliminate the zoning aspect and thus a whole separate tool to learn and use.<br />
      I&#39;ve also experienced more network issues with iSCSI as compared to FC, but they are generally much easier to troubleshoot with existing tools (like ping, traceroute, etc) versus having to break out one or more FC analyzers and pray you catch the issues.  So FC breaks a lot less but when it does it&#39;s a lot worse.<br />
      I believe the move to iSCSI is probably driven by cost than anything else at this point.  </p>
  - author: "Erwin van Londen"
    date: "03/15/2012 at 01:01 AM"
    html: |-
      <p>Hi Eric,</p>
      <p>I applaud your article and underlines what I&#39;ve always preached. </p>
      <p>FC comes out of the IPI enterprise space with leverage from the things of FDDI. It has been build from the ground up to be able to transfer channel protocols like SCSI,HIPPI,ESCON etc. The fact it also could transport TCP/IP was a bonus but not really spectacular. The IP FCP4 mapping  was written within a week. Besides that the different classes of service provides a very adaptable way of transporting upper layer protocols like SCSI, SBB, IP etc. (I think FC is the only protocol which provides a multicast service with guaranteed delivery.)</p>
      <p>There is a huge difference between network centric and channel centric transport. </p>
      <p>In my presentations and blogs I also pointed out that network people have a more horizontal view of the world whereas storage people have a vertical view. What I mean by this is the network people in general don&#39;t really care about IO profiles, block sizes, packet drops, in-order delivery etc but these are extremely important factors to storage people. That&#39;s the reason FC is the only protocol which is able to reliably steer these massive amounts of data back and forth. It is sheer impossible to achieve the same amount of data with the same accuracy and reliability with iSCSI as you can with FC.</p>
      <p>iSCSI was invented for server folks who needed a simple means of externally attached storage with minor or no investment to overcome the limitations of DAS. </p>
      <p>As for FCoE I think my standpoint is pretty clear. I don&#39;t really see the benefits above native FC beside the fact you need some fewer adapters and cables BUT from a support and troubleshooting perspective bolting one protocol on top of another is asking for more troubles and a significant longer recovery time especially when two &quot;sorts&quot; of people are involved (networking and storage).</p>
      <p>I&#39;ve seen many examples in my daily job when FCIP is involved where IP networks are used for remote replication. I predict similar issues will happen with FCoE.</p>
      <p>Again, Eric, I applaud this post and it proves that from a daily operations and a reliability perspective FC (even more so with TDZ) is a preferred way of managing storage.</p>
      <p>Also let me make clear that I&#39;m not saying one protocol or technology is better than the other but they do serve different purposes. Lets keep it that way.</p>
      <p>Regards,<br />
      Erwin van Londen</p>
      <p><br />
      </p>
  - author: "Erik Smith"
    date: "03/15/2012 at 08:06 AM"
    html: |-
      <p>Hi Chris, thanks for taking the time to provide the detailed feedback.</p>
      <p>I tried to keep the configurations as simple as possible and only included steps that are required.  Since VSANs are not even available on FC switch implementations other than Cisco, I didn&#39;t feel this fell into the required category and left those steps out.  Same type of response in regards to the zoning configuration I used.  </p>
      <p>In regards to iSCSI with Linux and Windows, these steps were captured a while ago and it&#39;s possible that additional support for the adapters I used has been included since then.  However, with Linux in particular, I installed SLES 11 SP1 a few weeks ago and noted that I still had to manually select the iSCSI components in order for them to be installed.</p>
      <p>In regards to ease of use, iSCSI definitely has the single management interface advantage, this is a big part of why I&#39;ve been pushing TDZ on FC/FCoE.  </p>
      <p>Finally, in regards to troubleshooting IP versus FC/FCoE, I have exactly the opposite opinion!  I suspect this has much more to do with background/experience/knowledge rather than anything inherent in the protocol, so I&#39;m willing to agree to disagree on that point.  </p>
      <p>Regards, Erik </p>
  - author: "Erik Smith"
    date: "03/15/2012 at 08:26 AM"
    html: |-
      <p>Hi Erwin, I agree with you on the protocol evolution aspects of your comments.  Actually, I&#39;ll have to take your word on some of those details because they were before my time.</p>
      <p>I think it&#39;s fair to say that people who work with block I/O tend to be more concerned with &quot;...IO profiles, block sizes, packet drops, in-order delivery etc...&quot; but there are big pockets of interest in this area in the traditional networking space.  One such area is WAN optimization but I&#39;m sure someone like Greg Ferro (see comment above) would be able to articulate it much better than I.</p>
      <p>Finally, in regards to your concerns about troubleshooting in an FCoE environment.  I&#39;ll agree that it can be more difficult at first, but once you get a handle on the basics, it&#39;s like anything else.. </p>
  - author: "WAN optimization"
    date: "03/26/2012 at 06:39 AM"
    html: |-
      <p>These kind of post are always inspiring and I prefer to read quality content so I happy to find many good point here in the post, writing is simply great, thank you for the post.</p>
  - author: "Skywalker"
    date: "05/28/2015 at 06:39 PM"
    html: |-
      <p>Need to add &quot;install &amp; configure multipathing software&quot; to the FC host deployment list</p>
  - author: "Erik Smith"
    date: "05/28/2015 at 06:59 PM"
    html: |-
      <p>Hi Luke?  <br />
      In any case, with regards to multipathing... Although it&#39;s not very realistic, all three of the protocols can work without multipathing, so I didn&#39;t include those steps for any of the protocols.</p>
---

<h3>Which is easier to use: FC, FCoE, or iSCSI?&#0160;</h3>
<p>This is the question we wanted to answer as we set out few months ago to test a series of nine configurations in the lab.&#0160; Our approach was to determine the number of provisioning steps required when using each protocol to connect to storage and then compare them.&#0160; We felt if one of the protocols was significantly more labor intensive than another, then perhaps this would shed some light on some of the recent trends we had been noticing.&#0160; Actually to put a sharper point on it, we wanted to determine why iSCSI seems to be more attractive than FC or FCoE in low end server virtualization environments.&#0160; A summary of the data we captured as well as the testing process used have been included below, but they were summed up perfectly by Mark Lippitt, one of EMC’s Distinguished Engineers, when he said something along the lines of:</p>
<h3>“FC and FCoE provisioning are <em><strong>Network-centric</strong> </em>and iSCSI provisioning is <em><strong>End-Node-centric</strong></em>.”</h3>
<p>Before I explain what he meant by this statement, let me start by stating (yet again), we don’t *really* care what protocol you use between your host and storage; we’ll support them all!&#0160; We do want to make sure that whatever protocol you have chosen to use is the best fit for your environment and it provides you with easy and error free operation.&#0160; Getting to the bottom of why iSCSI is successful in certain circumstances is important to us because it represents a change.&#0160;&#0160;</p>
<p>The testing results are shown the following table and I believe clearly show:</p>
<ol>
<li>Native FC requires the least number of configuration steps when compared with both iSCSI and FCoE.&#0160; </li>
<li>Configuring FCoE requires many more network configuration steps and requires fewer configuration steps on each individual host when compared with iSCSI.&#0160;&#0160;&#0160; </li>
<li>Configuring iSCSI requires much more work on each individual host and requires fewer configuration steps in the network when compared with FCoE.</li>
</ol>
<p>I’ll describe why this matters in a bit.</p>
<p><a href="/brasstacks/fc-and-fcoe-versus-iscsi-network-centric-versus-end-node-centric-provisioning/6a013487ed263f970c0167624c2a6d970b.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0167624c2a6d970b image-full" src="/brasstacks/fc-and-fcoe-versus-iscsi-network-centric-versus-end-node-centric-provisioning/6a013487ed263f970c0167624c2a6d970b.jpg" title="One" /></a></p>
<p>A few notes about the numbers in the table:</p>
<ul>
<li>The steps that were counted and entered into each cell have been included for your reference at the end of this post.&#0160; See “Configuration steps”</li>
<li>Since we had to deal with the comparison of “mouse clicks” and “CLI commands”, we tried to break them down into logical steps.&#0160; With the CLI this was basically one step for every CLI command.&#0160; For the GUI, we tried to count one step per dialog box unless I had to type in a value and then we counted each value entered as one step.&#0160; Perfect? No!&#0160; But we tried to be fair..</li>
<li>I have not counted steps that are common to all protocols such as attaching cables.</li>
<li>I’ve also included information that shows how <a href="/brasstacks/introducing-target-driven-zoning-tdz/" target="_self">TDZ</a> would reduce the total number of provisioning steps.&#0160; </li>
</ul>
<h3><strong>Getting to the point</strong></h3>
<p>As you may have noticed, in terms of the number of provisioning steps, the difference between FC, FCoE and iSCSI is not that great.&#0160; In fact, based on the numerous “FC is harder to use that iSCSI” complaints I’ve heard over the past couple of years, I was very surprised to see that FC requires 1/3 the number of configuration steps as iSCSI and I was also surprised to discover how many configuration steps are required to configure FCoE.&#0160; If you were just to look at these numbers you may come to the conclusion that FC is the clear winner and it will continue to dominate in the SAN, but then how do we explain iSCSI’s growth in the server virtualization space.&#0160; Obviously there are multiple factors at play but again Mark had a hypothesis about this that resonates as true to me “<strong>reducing the number of user interfaces is more important the reducing the total number of configuration steps”</strong>.&#0160; And this is where the concepts of “Network-centric” and “End-Node-centric” environments come into play.</p>
<h3><strong>Network-centric</strong></h3>
<p>FC and FCoE are Network-centric.&#0160; Both protocols rely on fact that the network will control what each end device has access to.&#0160; This control is centrally managed and requires a special set of FC skills to administer properly.&#0160; Since these are fairly specialized skills, I think you are more likely to find people that possess them in large organizations where controlling access to a pool of shared storage is a necessity.&#0160; In addition, since control is centrally managed, the end devices have evolved so that they will try and utilize every device that they can discover in the SAN.&#0160; This evolved behavior is one of the things that made the T11 FC-SCM technical report so difficult to write and unfortunately so un-implementable.&#0160; The bottom line is a Network-centric approach is probably better suited for large organizations that need centralized control of access to storage resources.&#0160;</p>
<h3><strong>End-Node-centric</strong></h3>
<p>iSCSI is End-Node-centric.&#0160; iSCSI relies on the fact that the network will allow communication between the iSCSI Initiator and whatever iSCSI Target the Server Admin points the Initiator at.&#0160; iSCSI requires no special set of FC SAN Administration skills, so it provides a very low hurdle for entry into the SAN space.&#0160; I suspect this low hurdle is the reason for uptick in iSCSIs adoption in the low end of the server virtualization space.&#0160; In addition, since control is managed at each individual end point, the end devices have evolved so that they will only discover what they are told to discover.&#0160; Maybe this partially explains why the iSCSI iSNS has been adopted by so few.&#0160; The bottom line is an End-Node-centric approach is probably better suited to smaller organizations that do not need centralized control of access to storage resources.&#0160;</p>
<h3><strong>LUN Masking</strong></h3>
<p>In both the Network-centric and End-Node-centric provisioning models, there is typically some kind of LUN Masking implemented on the storage array.&#0160; I suppose that this could be viewed as a centralized control of storage resource but since it is common across both iSCSI and FC/FCoE, I’m assuming that it would not influence the decision to use one protocol over another.&#0160;</p>
<h3><strong>Conclusion</strong></h3>
<p>So which one is right for you?&#0160;</p>
<p>I don’t know!&#0160; Figure it out for yourself!!! :-)</p>
<p>Seriously, it depends on what you need:</p>
<ul>
<li>if you require a separate high performance (up to 16GB/s) and fault tolerate SAN, then choose FC or FCoE. </li>
<li>If you are just entering into the SAN space and want to connect to your external storage without having to learn about FC/FCoE, then iSCSI is probably the best fit for you.</li>
<li>If you are somewhere in the middle, then it&#39;s mostly a matter of personal preference and you should choose what works best in your environment.&#0160; </li>
</ul>
<h3><strong>Topology tested</strong></h3>
<p>&#0160;<a href="/brasstacks/fc-and-fcoe-versus-iscsi-network-centric-versus-end-node-centric-provisioning/6a013487ed263f970c0168e74e0eb2970c.jpg" style="display: inline;"><img alt="Two" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0168e74e0eb2970c image-full" src="/brasstacks/fc-and-fcoe-versus-iscsi-network-centric-versus-end-node-centric-provisioning/6a013487ed263f970c0168e74e0eb2970c.jpg" title="Two" /></a></p>
<h3><strong>Configuration steps</strong></h3>
<p>Note: Please keep in mind that the steps listed below are just a description of&#0160;each task and do not necessarily represent all of the details required to complete&#0160;that particular task.&#0160; An example is “Install HBA”, obviously there is a reboot implied in this step.&#0160; I didn’t include all of the detail because the document that contains all of details was 50+ pages long..</p>
<h4>Hosts</h4>
<p>Windows:</p>
<p style="padding-left: 30px;">FC:</p>
<ol>
<li>Install HBA</li>
<li>Install Driver</li>
</ol>
<p style="padding-left: 30px;">FCoE:</p>
<ol>
<li>Install CNA</li>
<li>Install Driver</li>
</ol>
<p style="padding-left: 30px;">iSCSI:</p>
<ol>
<li>Locate the adapter that will be used for iSCSI in the “Network Connections” dialog</li>
<li>Right click the adapter, select properties, then select “TCP/IPv4” and click properties</li>
<li>Select “Use the following IP Address”</li>
<li>Enter an IP address</li>
<li>Enter a subnet mask</li>
<li>Enter a default gateway</li>
<li>Click OK and then close.</li>
<li>Install the Microsoft iSCSI Initiator software (can be downloaded from microsoft.com if necessary)</li>
<li>Open the Microsoft iSCSI Initiator properties dialog by clicking Start / Administrative Tools / iSCSI Initiator.</li>
<li>Add an iSCSI Target by clicking the Discovery Tab and then Add Portal…</li>
<li>Enter the IP Address of both iSCSI Targets into the “IP address or DNS name:” field as shown below:</li>
<li>Click Advanced and the Advanced Settings dialog is displayed</li>
<li>In the Local Adapter field, choose Microsoft iSCSI Initiator from the pull down list.</li>
<li>In the Source IP field, choose the IP Address of the Adapter that will be used to access this target.</li>
<li>Click OK and then OK again.</li>
<li>Click on the Targets tab and the iSCSI Targets should be displayed</li>
<li>Select the correct target in the list and then click Log on…, the Log On to Target dialog is displayed</li>
<li>Ensure that the Automatically restore this connection when the computer starts checkbox is selected.</li>
<li>Click OK.</li>
</ol>
<p>Linux:</p>
<p style="padding-left: 30px;">FC (FC drivers supported by EMC are inbox):</p>
<ol>
<li>Install HBA</li>
</ol>
<p style="padding-left: 30px;">FCoE (FCoE drivers supported by EMC are inbox):</p>
<ol>
<li>Install CNA</li>
</ol>
<p>&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;iSCSI:</p>
<ol>
<li>Download the appropriate driver</li>
<li>Unzip the driver</li>
<li>Install the driver and interact with installation script</li>
<li>Start the iSCSI driver</li>
<li>Verify the iSCSI driver was started </li>
<li>Edit the /etc/iscsi/iscsid.conf file and verify:</li>
<li>node.session.iscsi.InitialR2T is set to yes;</li>
<li>node.session.iscsi.ImmediateData is set to No; and</li>
<li>node.session.timeo.replacement_timeout is set to 60.</li>
<li>Set the run levels of the iSCSI daemon to automatically start at boot and to shut down when the server is brought down using chkconfig –level 345 iscsid </li>
<li>Assign an IP Address to the NIC that is to be used as the iSCSI initiator.</li>
<li>Use service network restart to allow the IP Address change to take effect.</li>
<li>Discover the Symmetrix iSCSI target using iscsiadm –m discovery –t st –p 10.246.54.109</li>
<li>Log into the storage using iscsiadm –m node –L all</li>
</ol>
<p>VMware:</p>
<p style="padding-left: 30px;">FC:</p>
<ol>
<li>Install HBA</li>
</ol>
<p style="padding-left: 30px;">FCoE:</p>
<ol>
<li>Install CNA</li>
</ol>
<p style="padding-left: 30px;">iSCSI:</p>
<ol>
<li>launch the vSphere client and login</li>
<li>Select a host from the inventory panel.</li>
<li>Click the Configuration tab and click Networking.</li>
<li>In the Virtual Switch view, click Add Networking.</li>
<li>Select VMkernel and click Next.</li>
<li>Select Create a virtual switch to create a new vSwitch.</li>
<li>Select a NIC to use for iSCSI traffic.</li>
<li>Click Next.</li>
<li>Enter a network label - A network label is a friendly name that identifies the VMkernel adapter that you are creating, for example, iSCSI.</li>
<li>Click Next.</li>
<li>Specify the IP settings and click Next.</li>
<li>Review the information and click Finish.&#0160; Verify the vSwitch that was created is show\</li>
<li>Select the host from the inventory panel of the vSphere client</li>
<li>Click on the configuration tab and then storage adapters.</li>
<li>Click on “add” above the storage adapters field and select Software iSCSI Adapter.&#0160; The iSCSI Software Adapter will be shown in the Storage Adapters section.</li>
<li>Select the iSCSI adapter and click properties in the details text area and the iSCSI Initiator Properties dialog is displayed.&#0160; </li>
<li>Click on the Network Configuration tab and then Add.&#0160; </li>
<li>Select the appropriate VMkernel Adapter and then OK.</li>
<li>Repeat for the other VMkernel Adapters.&#0160; When done, the iSCSI Initiator Properties dialog will appear as follows.</li>
<li>Click the Static Discovery tab and then click Add</li>
<li>Enter the IP Address of the iSCSI Target<strong> </strong>and it’s IQN.</li>
<li>Click OK.</li>
<li>Click OK and a rescan will be performed.&#0160; Once LUNs have been made available from the storage, perform a re-scan and devices should be visible from ESX.&#0160; </li>
</ol>
<p>Network – Not operating system specific:</p>
<p>FC:</p>
<p>Zoning:</p>
<ol>
<li>Create Zone</li>
<li>Add WWPN member 1</li>
<li>Add WWPN member 2</li>
<li>Add zone to configuration</li>
<li>Activate configuration</li>
</ol>
<p>FCoE:</p>
<ol>
<li>Enable FCoE Feature (one time)</li>
<li>system qos (The following QOS settings are done once)</li>
<li>service-policy type qos input</li>
<li>fcoe-default-in-policy</li>
<li>service-policy type queuing input</li>
<li>fcoe-default-in-policy</li>
<li>service-policy type queuing output</li>
<li>fcoe-default-out-policy</li>
<li>service-policy type network-qos</li>
<li>fcoe-default-nq-policy</li>
<li>vsan 600 (one time)</li>
<li>vlan 600 (one time)</li>
<li>fcoe vsan 600 (one time)</li>
<li>int vfc 5</li>
<li>bind int e1/5</li>
<li>switchport trunk allowed vsan 600</li>
<li>no shut</li>
<li>int vfc 6</li>
<li>bind int e1/6</li>
<li>switchport trunk allowed vsan 600</li>
<li>no shut</li>
<li>int e1/5</li>
<li>switchport mode trunk</li>
<li>switchport trunk allowed vlan 1, 600</li>
<li>spanning-tree port type edge trunk</li>
<li>int e1/6</li>
<li>switchport mode trunk</li>
<li>switchport trunk allowed vlan 1, 600</li>
<li>spanning-tree port type edge trunk</li>
<li>vsan database</li>
<li>vsan 600 interface vfc5</li>
<li>vsan 600 interface vfc6</li>
<li>Create Zone</li>
<li>Add WWPN of host</li>
<li>Add WWPN of target</li>
<li>Add zone to configuration</li>
<li>Activate configuration</li>
</ol>
<p>iSCSI:</p>
<ol>
<li>VLAN 700 (one time)</li>
<li>int e1/5</li>
<li>switchport access vlan 700</li>
<li>no shut</li>
<li>int e1/6</li>
<li>switchport access vlan 700</li>
<li>no shut</li>
</ol>
<p>Storage – Not protocol specific:</p>
<ol>
<li>Create the storage group</li>
<li>Add storage devices to the storage group</li>
<li>Create the port group</li>
<li>Add Symmetrix interfaces to the port group</li>
<li>Create the initiator group </li>
<li>Add the initiator to the initiator group</li>
<li>Create a masking view</li>
</ol>
<p>Thanks for reading!</p>
