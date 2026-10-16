---
title: "Introducing Target Driven Zoning (TDZ)"
pubDate: 2012-01-16
postedAt: "12:03 PM"
description: "At 9:28 on Tuesday 12/6/2011, the T11 FC-GS-7 working group approved a motion to incorporate the text for “Peer Zoning” that was prepared by Claudio DeSanti (Cisco). The actual text can be found in the T11 document 11-411v2. To me this moment marked the culmination of a four year journey..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2012/01/introducing-target-driven-zoning-tdz.html"
sources:
  - label: "Post and first page of comments"
    url: "https://web.archive.org/web/20240805000615/https://brasstacksblog.typepad.com/brass-tacks/2012/01/introducing-target-driven-zoning-tdz.html"
  - label: "Comments page 2"
    url: "https://web.archive.org/web/20220811140546/https://brasstacksblog.typepad.com/brass-tacks/2012/01/introducing-target-driven-zoning-tdz/comments/page/2/"
pdf: "/brasstacks/introducing-target-driven-zoning-tdz/introducing-target-driven-zoning-tdz.pdf"
comments:
  - author: "Stuart Miniman"
    date: "01/16/2012 at 12:33 PM"
    html: |-
      <p>Congratulations Erik - I know you put a time of energy and passion into this effort. As you said, hopefully customers will help move this from a good idea to real deployments.</p>
  - author: "Erik Smith"
    date: "01/16/2012 at 12:58 PM"
    html: |-
      <p>Thanks Stu! </p>
  - author: "Chris Carter"
    date: "01/16/2012 at 01:33 PM"
    html: |-
      <p>Congrats Erik (and others).  Sounds very useful to me.</p>
  - author: "Erik Smith"
    date: "01/16/2012 at 02:09 PM"
    html: |-
      <p>Thanks Chris!   </p>
  - author: "Victorforde"
    date: "01/16/2012 at 05:06 PM"
    html: |-
      <p>Excellent and interesting work!</p>
  - author: "Anthony Padula"
    date: "01/16/2012 at 07:13 PM"
    html: |-
      <p>Hi Erik, quick question about this.</p>
      <p>Will the storage port be able to remove peer zones when a WWPN is removed from the masking configuration?</p>
      <p>We still have upper limits on the number of zones in the fabric, and since this doesn&#39;t actually remove the requirement for the zone, we may still need to remove unused zones.  Especially in the case of a VMax, where every host WWPN is added to the masking configuration of every storage port in the masking view, this would actually increase the number of zones in each fabric.</p>
      <p>Great work by the way, this will be of great benefit once it becomes widely available.</p>
  - author: "Erik Smith"
    date: "01/16/2012 at 07:20 PM"
    html: |-
      <p>Thanks Victor!</p>
  - author: "Erik Smith"
    date: "01/16/2012 at 07:23 PM"
    html: |-
      <p>Hi Anthony, great question!  Yes, the peer zone will be updated each time the masking configuration changes.  Each change could represent the addition or removal of a host WWPN.</p>
  - author: "Scott DeShong"
    date: "01/17/2012 at 10:18 PM"
    html: |-
      <p>Erik,<br />
      How often would the array query the NS if a host is masked but is not yet powered on? If the NS doesn&#39;t have an entry would the zone still be created or would the array wait until it received an NS response that included the masked WWN? I like the overall idea but I see many organizations looking for the network team to take over SAN switch operations and having a storage admin who may or may not keep a consistent clean environment decide who can talk to what storage could be a scary proposition. I would prefer to see a little more intelligence related to removal of unused or inactive zones.</p>
  - author: "Willington Echeverri"
    date: "01/18/2012 at 07:29 AM"
    html: |-
      <p>Great work! Congratulations Erik.</p>
  - author: "Erik Smith"
    date: "01/18/2012 at 08:44 AM"
    html: |-
      <p>Hi Scott, thanks for the feedback!  The array port pushes peer members out to the switch (using AAPZ) when either:<br />
      1) The LUN Mask on the storage port changes; or<br />
      2) The array port detects that that current peer zone does not match the current masking database (using GAPZ)</p>
      <p>In the situation you are describing, there are at least four different scenarios that need to be considered:<br />
      a) The host port has never logged into the array port and its WWPN is not associated with a storage group.<br />
      b) The host port has never logged into the array port and its WWPN was manually added to the storage group.<br />
      c) The host port was previously logged into the array port and its WWPN is not associated with a storage group.<br />
      d) The host port was previously logged into the array port and its WWPN is associated with a storage group.</p>
      <p>Scenarios b and d would result in AAPZ being used as soon as the LUN Masking database was updated.  See update case 1 above.</p>
      <p>Scenarios a and c would result in no peer zone changes being made by the array port.</p>
      <p>In regards to house keeping tasks:<br />
      When a host adapter is replaced, it’s WWPN will change and this change will need to be reflected in the LUN Masking database, which will in turn be reflected in the peer zone members.  In other words the house keeping is done automatically for them.</p>
      <p>The peer zone will also be automatically updated if a storage group is destroyed due to a host being decommissioned.</p>
      <p>Does the approach described above fully address your concerns?<br />
      </p>
  - author: "Erik Smith"
    date: "01/18/2012 at 08:46 AM"
    html: |-
      <p>Thanks Willington!</p>
  - author: "mike warner"
    date: "01/18/2012 at 09:31 AM"
    html: |-
      <p>Nice work Erik! This will resolve a lot of issues in storage networking.</p>
  - author: "Erik Smith"
    date: "01/18/2012 at 11:29 AM"
    html: |-
      <p>Hi Mike, thanks!</p>
  - author: "Scott DeShong"
    date: "01/18/2012 at 12:00 PM"
    html: |-
      <p>Erik,<br />
      Thanks for the additional information. So if I&#39;m understanding correctly, the array will always implement zones for any defined storage group (configured LUN masking) regardless of host state. The zones will only change when the array masking changes.</p>
      <p>How would multiple arrays within the same fabric handle zoning? How would they agree on a common zoneset name? Would the GAPZ only check for zones in the active zoneset that match their respective LUN masking and ignore everything else? Would fabric locking be required to ensure only one array can update the zoneset at any one time?</p>
      <p>Thanks again for the great discussion!</p>
  - author: "Chris Conniff"
    date: "01/18/2012 at 01:01 PM"
    html: |-
      <p>Great Post Erik,  Let&#39;s hope that it becomes an approved AND accepted standard.  This way anyone that finds current zoning in a SAN difficult could give it a try instead of trying to run OLTP Apps on NFS!</p>
  - author: "Erik Smith"
    date: "01/18/2012 at 02:29 PM"
    html: |-
      <p>Hi Scott, thanks for the great questions!  These are points that I should have included in the original post.  </p>
      <p>You’re right; the peer zone members will always match the LUN mask.  </p>
      <p>In regards to your other points:  <br />
      1. Multiple arrays: Multiple arrays are allowed and this situation isn’t actually any different from the case where you have multiple ports from the same array attached to the same fabric because as of right now every array port will transmit its own AAPZ. </p>
      <p>2. Zone set names: By design the target port doesn’t have any knowledge of the zone set name.  The AAPZ simply requests that the fabric add a peer zone to the active zone set.  </p>
      <p>3. Zone Names: The target can specify any zone name desired, but this could lead to conflicts.  As a result, I’m pushing to have EMC Array ports just use the default zone name of X0_&#39;WWPN of principal device&#39;.  Since the WWPN of principal device is the same as the WWPN of the target port using the AAPZ and the WWPN is unique, we shouldn’t run into any zone name conflicts.<br />
      4. Fabric Locking: The fabric has to be locked every time the active zone set it modified.  This is an integral part of the three phase commit used today and was not something that could be changed.  As a result, AAPZ commands are accepted by the switch and then added to the active zone set at a later time.  The maximum amount of time between the AAPZ accept and when the change will actually take effect is one minute.  This one minute time period will allow the switches to coalesce AAPZ requests and it avoids zone set activation storms.  In practice, I am expecting the time between AAPZ and activation to be much less than one minute.        </p>
  - author: "Erik Smith"
    date: "01/18/2012 at 02:35 PM"
    html: |-
      <p>Hi Chris, thanks!  Agreed, accepted and requested by our customers is the next hurdle..</p>
  - author: "Sandeep MP"
    date: "01/22/2012 at 09:56 PM"
    html: |-
      <p>Congrats :)...<br />
      Looking forward to start working on this ..</p>
  - author: "Kiran Kumar"
    date: "01/31/2012 at 09:37 AM"
    html: |-
      <p>Its perfect and too interesting..</p>
  - author: "sreejith"
    date: "02/08/2012 at 01:02 PM"
    html: |-
      <p>This is superb Stuff :) .Article was very informative.I have two questions <br />
      1.How this is going to work with auto provisioning in VMAX models ?<br />
      2.Since zoning is done at storage port level ,does current storage processors support this technology ,i am pretty sure this will create more problems if front end port is dead,either we cant access storage nor we cant do zoning ? </p>
      <p>Regard&#39;s<br />
      Sreejith.C</p>
  - author: "Erik Smith"
    date: "02/10/2012 at 08:53 PM"
    html: |-
      <p>Hi Sreejith, thanks!  </p>
      <p>In regards to question 1, the actual implementation details are still being worked out.  As soon as I have a better feeling for how this will be integrated into the UI, I will be doing another post.  </p>
      <p>For question 2, there is nothing to prevent you from making the same storage device visible on multiple interfaces and then using something like PowerPath for load balancing and failover.  Also, traditional fabric based zoning will still function as it does today, so you can always fallback to that if necessary.</p>
      <p>Regards, Erik <br />
      </p>
  - author: "sreejith"
    date: "02/13/2012 at 06:01 AM"
    html: |-
      <p>Thanks Eric ,<br />
      I&#39;m pretty sure this will be a turn around .I wish you all the best :)<br />
      </p>
  - author: "Chris Norris"
    date: "02/15/2012 at 02:36 PM"
    html: |-
      <p>Great article Erik, I would very much like to see this technology adopted!</p>
      <p>Has there been any thought given to how this could play into multi switch fabrics?  Would ISL&#39;s still be configured by hand or does this contain provisions for switches to identify and proliferate zones to peer switches?</p>
  - author: "Erik Smith"
    date: "02/16/2012 at 09:45 AM"
    html: |-
      <p>Hi Chris, thanks! </p>
      <p>Since a Peer Zone is literally a zone tagged with a special attribute, it will be automatically distributed throughout the fabric as a part of the zone set / configuratoin just like a traditonal zone would be.</p>
      <p>Physical ISLs would still need to be present (and configured) but if you were using VSANs, one could easily imagine a way to automatically configure IVR to allow the connectivity specified by the target.  This is actually a very interesting idea...</p>
  - author: "Dave Silvestri"
    date: "02/16/2012 at 10:39 AM"
    html: |-
      <p>Following up on sreejith&#39;s comments...</p>
      <p>If you define masking in an autoprovisioning group (not exclusive to VMAX, other vendor&#39;s have initiator groups as well), would zoning be identical between fabrics?</p>
      <p>For example:<br />
      - an IG of 2 initiators (1 per fabric)<br />
      - a PG of 2 ports (1 per fabric) <br />
      - a SG of x devs<br />
      - MV of the above</p>
      <p>Would there be 4 zones in each fabric? Or would TDZ only create zones in it&#39;s fabric for the WWNs that it can locate? I believe it&#39;s the latter, but want to double check.</p>
      <p>I may have missed something, I need to read the article again, lots of great info here.</p>
      <p>Great article to be clear.</p>
  - author: "Erik Smith"
    date: "02/16/2012 at 02:25 PM"
    html: |-
      <p>Hi Dave, thanks!  Peer zoning would allow either of the behaviors you are describing. As a result, I view this decision as an implementation detail.  I can see arguments for and against both approaches.  Do you have a strong preference towards one or the other or will either work?</p>
  - author: "Dave Silvestri"
    date: "02/17/2012 at 11:59 AM"
    html: |-
      <p>Personally I prefer to keep my zoning specific to the entities that exist in a fabric. I find it helps if someone does upgrades on a server and pulls the fibre cables, and then replaces them when complete, but gets them reversed.</p>
      <p>Mostly that&#39;s for names/nicknames (which I also wonder if you could pull from the masking consistency is wonderful). </p>
      <p>I suppose a benefit is that it wouldn&#39;t matter if the cables got reversed... however I prefer symmetry, and all my &quot;a&quot; labeled hbas on fabric A, and all my &quot;b&quot; labeled hbas on Fabric B... </p>
      <p>To each his own though :)</p>
  - author: "Erwin van Londen"
    date: "03/15/2012 at 01:40 AM"
    html: |-
      <p>:-) Very nice to see it finally got accepted and written up by T11. Coincidence is that I had a similar proposal back in 2002 when doing consulting work for HP and had a long discussion with one of the HP engineer in Colorado Springs.</p>
      <p>I asked once or twice how it went but when push came to shove other projects were given priorities and the idea lead to lala land. In this case your ears. :-)</p>
      <p>Anyway, great job Eric and I hope to see this coming in array/switch implementations in the very near future. Will save many people a lot of headaches. :-)</p>
  - author: "Erik Smith"
    date: "03/15/2012 at 08:42 AM"
    html: |-
      <p>Hi Erwin, thanks!  For our customers sake, I wish you had succeeded earlier!  I think it would have made FC much easier for them to use...</p>
      <p>Regards, Erik   </p>
  - author: "Sreejith.c"
    date: "03/23/2012 at 09:20 AM"
    html: |-
      <p>Thank you Erik :) Appreciate your reply <br />
      </p>
  - author: "MGK"
    date: "01/09/2013 at 08:17 AM"
    html: |-
      <p>Any progress on this really interesting topic?</p>
  - author: "Erik"
    date: "01/17/2013 at 08:17 AM"
    html: |-
      <p>Hi Michal, yes we&#39;re making progress on TDZ.  I hope to have something significant to share in the next few days.</p>
      <p>Erik </p>
  - author: "Mallik"
    date: "07/07/2014 at 01:44 AM"
    html: |-
      <p>Hello Erick,</p>
      <p>its a brilliant idea and significant savings from a operational perspective.</p>
      <p>may i know how its making progress in terms of implementation by storage vendors (EMC, Cisco, Hitachi)? </p>
      <p>Thanks,<br />
      Mallik. </p>
  - author: "Erik Smith"
    date: "07/07/2014 at 10:27 AM"
    html: |-
      <p>Hi Mallik, thanks!  I was pleasantly surprised with all of the attention TDZ recieved at EMC World this year.  Although interest from our Customers (and competition) is way up compared to a year ago, I cannot share anything specific about our product plans at this point.  I can say the amount of time I&#39;ve been spending on it recently has dramatically increased but its too early to say what will come of that effort.  </p>
  - author: "IgalK"
    date: "09/25/2016 at 03:52 AM"
    html: |-
      <p>Hello Eric,</p>
      <p>As the concept of TDZ is still interesting to me, now, about 4 Years after, I wonder what was the popularity and the adoption rate by the customers?</p>
      <p>Thanks,<br />
      Igal</p>
  - author: "Erik Smith"
    date: "09/27/2016 at 09:51 AM"
    html: |-
      <p>Hi Igal, although Brocade has supported TDZ since FOS 7.4 and I know at least one of our competitors support it as well, I don&#39;t have any information about actual adoption.  Once our storage arrays support the feature, we&#39;ll have a better idea of actual adoption and I&#39;ll provide an update at that point.</p>
---

<p>At 9:28 on Tuesday 12/6/2011, the T11 FC-GS-7 working group approved a motion to incorporate the text for “Peer Zoning” that was prepared by Claudio DeSanti (Cisco).&#0160; The actual text can be found in the T11 document 11-411v2.&#0160; To me this moment marked the culmination of a four year journey to take a concept, get it through a standards body and into a standards document.</p>
<p>Target Driven Zoning (TDZ) is a proposed application that utilizes Peer Zoning <strong>to reduce the number of steps required to provision new storage by 50%.</strong>&#0160; Since many customers have been complaining about the task of zoning for years, <strong>I’m proposing to achieve this reduction by eliminating the manual task of FC zoning</strong>.&#0160;</p>
<p>Just to be clear, while I view introduction of the Peer Zoning functionality as a game changer for FC, I don’t view the completion of this effort as some kind of extraordinary accomplishment, actually there’s nothing extraordinary about it.&#0160; These sorts of efforts are started all the time in standards bodies.&#0160; Sometimes&#0160;they result in useful&#0160;protocols that are implemented by&#0160;many (e.g., FCoE and FIP).&#0160; Other results&#0160;are implemented by few but they provide a critical requirement for the industry (e.g., FC-SP) and yet others&#0160;turn out to be&#0160;interesting academic exercises but are never implemented by anyone (e.g., FC-SCM).&#0160; I have hopes that Peer Zoning will fall into the category of “useful technology that is implemented (and deployed) by many” but it’s too early to tell as this point.&#0160;</p>
<p>This post is intended to give you an overview of the technology and give you enough information to decide if TDZ is something that you’d like to use in your environment.&#0160; I also feel it’s important to give credit where it’s due and with that in mind without the help of Mark Lippitt, David Black, Claudio DeSanti, Bob Nixon and Ralph Weber; this entire effort would still be hopelessly stalled.&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;</p>
<p><span style="text-decoration: underline;"><span style="font-size: 12pt;"><strong>Background</strong></span></span></p>
<p>The story starts back in mid-2007.&#0160; I was on a conference call with David Black and Mark Lippitt (both with EMC) discussing what would happen if zoning wasn’t used in an FC SAN (as was being proposed in the T11 FC-SCM working group).&#0160; In case you don’t know, EMC has a fairly strict best practice called “Single Initiator Zoning” that was created based on lab testing results.&#0160; As the name suggests, the best practice states “zones should only contain a single initiator as well as the storage targets it needs to access.”&#0160; Because of the work that I had done with fabric scalability, I was pulled into the meeting (somewhat last minute if memory serves) and asked to provide my opinion on what was being proposed.&#0160; Now, as most people who work with me will tell you, I typically call things as I see them and the intensity of my voice will vary with the level of conviction that I feel about a given topic.&#0160; As a result, my reaction to eliminating zoning was something along the lines of “ARE YOU&#0160;&lt;bleep&gt; KIDDING ME?” and I proceeded to provide specific reasons why I thought that this was the *SILLIEST* idea I had ever heard of.&#0160; Perhaps it was the intensity of my reaction (or the simple fact that David simply didn’t have sufficient bandwidth to create a presentation that contained all of my points), in either case, he eventually asked me to present my list of concerns to the T11 FC-SCM working group at the August 2007 meeting in Seattle.&#0160;</p>
<p><span style="text-decoration: underline;">Preparing for Seattle</span></p>
<p>In case you aren’t familiar with T11, this is the group that literally wrote the book on FC.&#0160; In fact, a better way to say it would be they ARE the book.&#0160; From my point of view as an integration engineer who “grew up” with FC, the idea of merely attending (let alone presenting at) this meeting felt something akin to traveling to Mt Olympus and meeting Zeus and the gang. &#0160;As a result, I spent much of the month before the meeting preparing by testing specific “unzoned” configurations in the lab, re-reading the various standards involved (FC-GS and FC-SW), iterating on the presentation with Mark Lippitt and working myself up into an emotional wreck in general.&#0160; As luck would have it, the FC-SCM meeting was first on the schedule for the week, so off I went to present at my first T11 meeting without having actually ever attended one.&#0160;</p>
<p><span style="text-decoration: underline;">The FC-SCM meeting</span></p>
<p>During the FC-SCM meeting I presented “FC-SCM-OpenZoning”.&#0160; The main point of the presentation was <strong>due to the way Initiators and Targets perform discovery, you can’t simply eliminate zoning</strong>.&#0160; If you did, the resulting flood of name server queries every time something changed in the fabric would bring the fabric to its knees with as few as 255 N_Ports in the fabric.&#0160; Consider the case where an N_Port is bouncing (logging in an out) and you are <span style="text-decoration: underline;">totally screwed</span>.&#0160; After speaking to my last slide and answering a couple of questions, I returned to my seat feeling like the weight of the world had been lifted off of my shoulders.&#0160; I think Mark Lippitt and David Black said something to the effect of “Nice job” and my response was going to be “Boy, am I glad that’s over with” but before I could even get the words out of my mouth, Claudio turned around and said something to the effect of “Ok, so you have shown us a problem, now what?&#0160; Would you be willing to come back and present a solution?”&#0160; I literally couldn’t believe my ears, I was like “are you talking to me?”&#0160; After briefly consulting with Mark, I said yes and committed to provide a proposal at the October 2007 T11 meeting in Coeur d’Alene, ID.&#0160; The purpose of that proposal would be to describe an approach that would eliminate the manual task of zoning.</p>
<p><span style="text-decoration: underline;">Inspiration strikes</span></p>
<p>After the FC-SCM meeting Mark, David and I went out to lunch.&#0160; On the walk down to Pike’s Place Market I was walking behind them while they were talking about the concept of OLZ or “One Large Zone” (what would eventually become FC-SCM).&#0160; I found OLZ interesting and would dedicate many hours over the next three years pushing it for it to be adopted, but I wanted to pursue a different approach.&#0160; I believed (and still do) that the key to a solution was to solve the RSCN problem.&#0160; Basically, the RSCN problem happens in an environment without zoning when a single device logs in or out.&#0160; When the device’s status changes an RSCN is sent to all devices that are impacted by the change.&#0160; Since all devices register for RSCN in a fabric without zoning, every device would receive an RSCN and would pile on the Name Server at the same time and basically cause a DoS attack.&#0160; With this concern in mind my thinking process went something along the lines of:</p>
<p><strong>What if somehow we could send RSCNs only to end devices that are actually impacted by the change (i.e., hosts that are logged into that target and vice versa)?</strong></p>
<ul>
<li>Where would this information come from?</li>
</ul>
<p><strong>Maybe a storage port could tell the switch to only send RSCNs to end devices that are logged into it?</strong><strong> </strong></p>
<ul>
<li>You would probably identify these devices to the switch by their WWPN</li>
</ul>
<p><strong>But wait a second, our storage ports have a list of WWPNs that they care about (have been granted access) in the LUN masking database</strong></p>
<ul>
<li>If a storage ports could somehow send these WWPNs to the switch…</li>
<li>A switch could use this information to restrict RSCN distribution</li>
</ul>
<p><strong>But…switches already use the WWPNs in the definition of a zone</strong></p>
<p><strong>Why couldn’t the storage port just share the WWPNs in the LUN Masking database with the switch and then the switch could just create the zones based on this information???</strong></p>
<p><span style="text-decoration: underline;">The rest of the story</span></p>
<p>Describing all the ups and downs of the story goes way beyond the scope of this post, but a couple of excerpts from a cliff notes version would certainly mention; Claudio agrees to write the text at the August 2011 meeting in Edmonton, delivers the goods in Albuquerque and it all gets approved in St. Petersburg.&#0160; Thanks again Claudio!&#0160;</p>
<p><span style="text-decoration: underline;"><strong>Target Driven Zoning technical details</strong></span></p>
<p>In this section I describe how I envision the Peer Zoning functionality Claudio defined in 11-411v2 will be utilized by an application that I am calling Target Driven Zoning or TDZ.</p>
<p><strong>The Target Driven Zoning concept is simple, since a storage port has all of the information required to create an FC zone, it should just go ahead and create one automatically</strong>.&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;</p>
<p>Before I dive into the protocol level details that will explain how TDZ works, let me take step back and define the Storage Provisioning process as it is done today without TDZ and then show how it would work with TDZ.</p>
<p><span style="text-decoration: underline;">Without TDZ </span></p>
<ol>
<li>Physically attach hosts and storage to the fabric.</li>
<li>Using the switch zoning interface, create a zone that contains an initiator and its targets.&#0160; Repeat for every initiator/target relationship being added to the environment.</li>
<li>Activate the new Zone Set / Configuration.</li>
<li>Using the Storage array management interface, add each initiator to a “Storage Group” on the array.</li>
</ol>
<p><span style="text-decoration: underline;">With TDZ</span></p>
<ol>
<li>Physically attach hosts and storage to the fabric.</li>
<li>Using the Storage array management interface, add each initiator to a “Storage Group” on the array.&#0160; <strong>The storage will then automatically setup the appropriate zones to allow each initiator to access it.</strong></li>
</ol>
<p><span style="text-decoration: underline;">The nuts and bolts of Peer Zoning / TDZ</span></p>
<p>For the remainder of this section, I’ll be referring to the following configuration.&#0160; Starting from the left, the configuration consists of:</p>
<ol>
<li>A Host containing a single HBA/CNA port that has a WWPN (World Wide Port Name) of 10:00:00:00:00:00:00:00.&#0160;&#0160; </li>
<li>A FC Fabric containing two FC switches: <ol>
<li>FC/FCoE Switch Domain 3; and </li>
<li>FC/FCoE Switch Domain 4</li>
</ol></li>
<li>A Storage array containing a port that has a WWPN of 50:00:09:71:20:30:40:50</li>
</ol>
<p><a href="/brasstacks/introducing-target-driven-zoning-tdz/6a013487ed263f970c0168e5a1d34c970c.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0168e5a1d34c970c image-full" src="/brasstacks/introducing-target-driven-zoning-tdz/6a013487ed263f970c0168e5a1d34c970c.jpg" title="One" /></a></p>
<p><span style="text-decoration: underline;">Step 1 – The Target queries the Unzoned Name Server</span></p>
<p>Due to an assumption on our part of “when creating a Storage Group, users would rather pick WWPNs from a list rather than manually type them in”; TDZ suffers from a causality dilemma that is solved by utilizing the unzoned name server.&#0160;&#0160;</p>
<p>The dilemma is:</p>
<p><em>How do you pick a host WWPN from a list in the array’s management software when none of the interfaces on that array have been zoned to have access to that host WWPN?</em></p>
<p>As I describe in the <a href="/brasstacks/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san/" target="_blank">Hard zoning versus Soft zoning blog post</a>, the response from the switch to a Name Server query will usually only contain those devices that share a common zone with the querying N_Port.&#0160; When TDZ is being used, there is a very good chance that the storage has not been zoned to have access to anything.&#0160; As a result, it will not be possible to provide a list of initiator WWPNs to the storage admin via a traditional NS query.&#0160; &#0160;&#0160;</p>
<p>&#0160;</p>
<p>The unzoned Name Server provides a solution to this dilemma because as the name implies, the unzoned name server allows an N_Port to query the Name Server and obtain a list of all N_Ports registered with the fabric without regard for zoning.</p>
<p><span style="text-decoration: underline;">Step 2 – The Name Server returns a list of all ports registered in the Fabric</span></p>
<p>The response to the unzoned Name Server query will be a list of all N_Ports registered with the fabric.&#0160;</p>
<p>As you think about this behavior, you may come to the conclusion that it represents a serious security flaw.&#0160; As Peer Zoning was being defined, we felt the question we needed to answer was:</p>
<p>“If any N_Port can just query the unzoned Name Server, what’s to stop a host from using the unzoned name server to discover what targets are out there and then grant itself access to any storage port that it wants?”&#0160;</p>
<p>We thought about this question (a lot actually) and we came up with a multi-pronged approach.&#0160; As I’ll describe shortly each approach represents a different level of security that can be set on a fabric wide basis.&#0160; However, before I get to the descriptions, let me state that no matter which one you choose, you are still protected by LUN Masking on the Storage array.&#0160; In other words, if a rogue host were to grant itself access to the target using Peer Zoning commands, the rogue host would still be prevented from accessing data on that target due to LUN Masking.&#0160; LUN Masking will only allow certain WWPNs to access certain LUNs on each target.&#0160; So even if a host created a zone to allow itself to have access to a target port, it would also need to spoof the WWPN of a host that has been granted access to LUNs on that target.&#0160; Let me point out that this is something that can easily be done today on all HBA and CNAs and does not represent a new security hole that is being introduced by peer zoning.&#0160;</p>
<ul>
<li>Option 1: Peer Zoning disabled (default).&#0160; If you don’t find manual zoning tasks to be too much trouble, then you can opt not to enable peer zoning.</li>
<li>Option 2: Peer Zoning enabled – Authentication required.&#0160; This option allows you to enable Peer Zoning but will require any port that wants to use the unzoned Name Server to authenticate with the switch using one of the mechanisms defined in FC-SP (e.g., DH-CHAP)</li>
<li>Option 3:&#0160; Peer zoning enabled – Port based.&#0160; This option allows you to enable Peer Zoning but it will only allow unzoned name server queries on certain switch interfaces.&#0160; You could simply enable the feature on interfaces where storage ports are located.</li>
<li>Option 4: Peer zoning enabled – OUI based.&#0160; This option allows you to specify that certain vendor OUI’s can use unzoned Name Server queries by default.&#0160; (e.g., I trust &lt;your storage vendor of choice&gt; (hopefully EMC) OUIs but not others)</li>
<li>Option 5: Peer zoning enable – open.&#0160; This option allows you to specify that Peer Zoning can be used by any N_Port in the fabric.</li>
</ul>
<p><span style="text-decoration: underline;">Step 3 – The Storage Admin attaches the correct host WWPN to a “Storage Group”</span></p>
<p>This is more of a Storage Provisioning process step and does not require any FC protocol interaction.&#0160; From within the Storage Array software application, the storage admin selects a host and associates it with a “Storage Group”.&#0160; When the user clicks “OK” or something similar, the next step will be performed.</p>
<p><span style="text-decoration: underline;">Step 4 – The Storage port uses AAPZ</span></p>
<p>Once the Storage Administrator adds the WWPN of the host to the storage group and commits this change, the storage port(s) that are associated with this storage group will use AAPZ (Add/replace Active Peer Zone) to add the appropriate peer zones to the fabric.&#0160; The AAPZ request will contain the zone name, the principal N_Port name as well as the zone members (the peers) that should be allowed to access the principal N_Port name.</p>
<p><span style="text-decoration: underline;">Step 5 – The AAPZ is accepted by the switch</span></p>
<p>Assuming the switch is functioning properly and it is not too busy to process the AAPZ, it will accept the AAPZ.&#0160;</p>
<p><span style="text-decoration: underline;">Step 6 – New zoneset / configuration is activated on the fabric by the switch </span></p>
<p>The Once the switch transmits the ACC to the AAPZ, it has one minute to actually update the zoning on the fabric.&#0160; An example of a peer zone is shown at the top of the following diagram.&#0160;</p>
<p>&#0160;<a href="/brasstacks/introducing-target-driven-zoning-tdz/6a013487ed263f970c016760a1141b970b.jpg" style="display: inline;"><img alt="Two" border="0" class="asset  asset-image at-xid-6a013487ed263f970c016760a1141b970b image-full" src="/brasstacks/introducing-target-driven-zoning-tdz/6a013487ed263f970c016760a1141b970b.jpg" title="Two" /></a></p>
<p><span style="text-decoration: underline;">Step 7 – RSCNs distributed to all affected N_Ports</span></p>
<p>Once the zone set containing the new Peer Zone has been activated onto the fabric, each switch will transmit RSCNs to each affected N_Port.&#0160; By the way, there is nothing new here.&#0160; RSCNs are an existing part of the FC protocol and are widely used today.</p>
<p><span style="text-decoration: underline;">Step 8 – The Host performs FC discovery</span></p>
<p>Once the hosts in the peer zone have received an RSCN, they will perform FC discovery as normal.&#0160; This is the same discovery process that I described in the <a href="/brasstacks/hard-zoning-versus-soft-zoning-in-a-fcfcoe-san/" target="_self">Hard versus soft zoning blog post </a>with one big exception; the peer members in a peer zone are only allowed to access the principal zone member and not each other.&#0160; This is a new behavior specific to peer zones and it is was put in place to ensure that our single initiator zoning best practice can remain intact.&#0160;&#0160;&#0160;</p>
<p><span style="text-decoration: underline;">Step 9 – Storage verifies zoning via GAPZ</span></p>
<p>At any point after using AAPZ, a target port can use GAPZ to verify that the zoning change is in place.</p>
<p><strong>Conclusion</strong></p>
<p>If you’re interested in hearing more about TDZ or are an EMC Customer and interested in actually giving it a try, please let me know!&#0160; A robust amount of Customer demand is all that is required to get this idea out of the prototype phase and into the ready to deploy phase.</p>
<p>Thanks for reading!</p>
