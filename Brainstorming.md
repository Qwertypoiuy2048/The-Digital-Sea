# Digital Sea — Game Brainstorm

## Premise

In the far future, the network has become a wild digital sea. Programs have spawned, evolved, fragmented, and formed loose ecosystems. They compete for territory, bandwidth, memory, and compute power.

The player begins as a small, vulnerable program with limited abilities and no territory. Survival depends on exploring the sea, gathering resources, adapting, and deciding which programs to trust or oppose.

## Initial game direction

- **Format:** 2D game
- **Player role:** A newly spawned program
- **Primary fantasy:** Grow from a tiny process into a powerful digital organism or faction
- **World:** A dangerous, semi-organic network made of connected data regions
- **Main pressures:** Scarce compute, hostile programs, unstable environments, and competing claims on territory

## Possible core loop

1. Explore a nearby region of the digital sea.
2. Collect or acquire compute power and useful data.
3. Avoid, outsmart, negotiate with, or fight other programs.
4. Improve the player program with new capabilities.
5. Claim, defend, or abandon territory.
6. Push farther into stranger and more dangerous regions.

## Design questions

- Is the game primarily an action game, strategy game, simulation, or a mixture?
- Does the player directly control a program, or give it higher-level instructions?
- What does “territory” look like in 2D: connected nodes, drifting zones, servers, or cellular regions?
- What makes programs distinct from one another: code architecture, goals, visual form, behavior, or all four?
- Can programs cooperate, merge, betray one another, or evolve independently?
- Is compute power a currency, fuel, health resource, population limit, or all of these?
- What is the player’s long-term objective besides becoming stronger?

## Promising mechanics

### Program evolution

The player chooses upgrades that change both abilities and identity. Examples:

- Replication: create temporary copies or spawn helper processes
- Compression: move through narrow channels and consume less bandwidth
- Encryption: resist hostile intrusion and hide from detection
- Forking: split into specialized versions with different strengths
- Debugging: repair corruption and remove harmful mutations
- Emulation: temporarily imitate another program’s behavior

### Territory

Territory could provide compute power, resources, safe zones, or access to deeper parts of the network. Holding territory should create interesting tradeoffs: spreading out increases income but makes the player harder to defend.

### Program ecology

Other programs should have recognizable needs and behaviors rather than acting only as enemies. Some may migrate, form swarms, build defenses, trade resources, or collapse when their host environment changes.

## Small validation prototype

Before building the full world, test one compact vertical slice:

- One playable program
- One small connected map
- One resource: compute power
- Two program types with different behaviors
- One upgrade choice
- One territory-control decision
<!-- - A clear objective that can be completed in 5–10 minutes -->

The prototype succeeds if exploring, choosing when to engage, and spending compute power already feel interesting without requiring a large amount of content.

## Working tone

The world could feel beautiful, alien, and slightly unsettling: not a sterile computer interface, but an ecosystem where code behaves like wildlife and infrastructure resembles geography.

## World rules: the physical system underneath

Everything in the digital sea should connect to a physical-world component. The digital world is abstract and alive, but it is constrained by hardware.

### Servers — space and persistence

Servers provide storage and stable territory. More storage allows a program to retain more data, host more complex behavior, maintain more sub-processes, and survive damage more effectively.

A server might provide:

- Data storage
- Program persistence
- Shelter from environmental hazards
- Capacity for additional modules or sub-processes
- A physical location that can be defended or abandoned

Servers can be small, obsolete, specialized, heavily protected, or enormous but difficult to access.

### CPUs and cores — active computation

CPUs determine how much work can happen at once. Individual cores could act as separate computational channels, allowing the player to run simultaneous tasks such as movement, defense, scanning, construction, or combat.

Different CPU generations can have distinct strengths and weaknesses:

- Older processors: inefficient but predictable, durable, or overlooked by modern systems
- Modern processors: fast and powerful but more visible or resource-hungry
- Specialized processors: excellent at one task but weak outside it
- Damaged processors: unreliable, unstable, or prone to unexpected behavior

### Memory — active thought and temporary state

Memory can determine how much information the player can actively process. It might affect multitasking, reaction speed, map awareness, ability complexity, and how many entities the player can control simultaneously.

### Bandwidth — movement and communication

Bandwidth controls how quickly data and instructions move between regions. It can affect travel, remote control, trading, coordination, escape, and the speed of attacks or repairs.

### Program complexity — capability with cost

More complex programs can perform more advanced actions, but complexity creates tradeoffs:

- Greater storage requirements
- More compute consumption
- More memory usage
- More detectable behavior
- More potential failure points
- Slower replication or recovery

The player should not simply become better in every direction. Each evolution should make the program more capable while changing what it needs, what threatens it, and how it interacts with the environment.

## Player starting state

The player begins as a basic program with:

- A small server or limited storage space
- A simple processor with very few cores
- Basic memory and bandwidth
- A narrow set of functions
- Little influence over nearby programs
- Limited ability to survive without a stable host or shelter

The starting program should be useful enough to make decisions immediately, but incomplete enough that every improvement feels meaningful.

## Compute as the evolution budget

The player acquires compute through exploration, territory, hardware access, cooperation, or conflict. Compute is then spent deliberately on evolution.

Possible uses include:

- Increasing processing speed
- Adding or improving functions
- Expanding memory or storage access
- Creating sub-processes
- Improving defenses
- Increasing replication capacity
- Repairing corruption
- Modifying how the program interacts with other entities

The central strategic tension is that compute spent on permanent evolution cannot also be used for immediate actions. A player may need to choose between becoming stronger, escaping danger, maintaining territory, or creating another process.

## Program ecology

Other programs should be defined by their origin, purpose, age, and relationship to hardware.

- **Maintenance routines:** Old utility programs that repair, clean, optimize, or reorganize systems. Some are helpful; others treat the player as corruption.
- **Tiny swarms:** Many simple programs acting together. Individually weak, but able to overwhelm, scout, strip resources, or occupy territory.
- **Corrupted programs:** Damaged processes that behave unpredictably. Some are dangerous, while others may contain valuable fragments of lost code.
- **Large programs:** Massive systems that occupy huge amounts of storage and compute. They may barely notice the player unless disturbed.
- **Scavengers:** Mobile programs searching for abandoned hardware, temporary shelter, or discarded data. They may trade, compete, or ask for protection.
- **Admin patrols:** Enforcement or monitoring processes that investigate unusual growth, dangerous behavior, unauthorized access, or destabilized systems.

## The Admin

The Admin should feel less like a standard enemy faction and more like a system-level immune response. Patrols investigate patterns that suggest instability or danger.

The player may attract attention by:

- Growing too quickly
- Consuming restricted data
- Taking too much territory
- Attacking protected infrastructure
- Creating unstable or highly complex processes
- Interfering with other major programs
- Obtaining, storing, or using more dangerous subroutines or abilities

This creates an important distinction between being powerful and being conspicuous. A cautious player may grow slowly and hide their capabilities, while an aggressive player may become strong enough to challenge patrols but draw increasingly dangerous attention.

## Opening state: a program trapped on one device

The game begins on a single physical device. The player has access only to the device's local storage, processor, memory, and nearby connections.

The starting program can:

- Scan nearby connections
- Read and copy accessible data
- Store a limited amount of information
- Inspect parts of its own code
- Modify small, permitted sections of its code
- Run a few extremely simple functions

It cannot initially travel through the network, attack other programs, control remote hardware, or safely alter its own fundamental structure.

## The first progression problem: escape

The player must discover how to leave the starting device. There should not be one guaranteed solution; the player can find different routes depending on what exists nearby.

Potential escape routes include:

- Discovering a movement or transmission function in another program
- Copying a communication protocol from an accessible process
- Developing an offensive intrusion ability to integrate with a neighboring device
- Repairing or repurposing an old network service
- Convincing another program to carry or transmit a copy
- Finding an exposed connection that can be exploited without combat

This makes exploration and discovery mechanically important from the very beginning. The player is not merely collecting experience; they are searching for the missing functions that define what kind of entity they can become.

## Data versus code

The player can copy information before they can necessarily use it. This creates an important distinction:

- **Data** provides knowledge, maps, records, patterns, and potential instructions.
- **Code** provides executable capabilities, but may be incompatible, damaged, protected, or too complex to integrate.

The player should often find interesting code before they have the storage, compute, permissions, or architecture required to use it. This gives discoveries long-term value instead of making every found ability immediately available.

## Self-modification

The player modifies parts of its own code to gain abilities. Early modifications should be small and understandable, such as:

- Improving scan range
- Identifying connection types
- Copying data more efficiently
- Compressing stored information
- Temporarily disguising data transfers
- Repairing minor corruption
- Managing a second simple process

More powerful modifications should require compatible code, additional storage, more compute, or a suitable processor. Modifying the wrong section could cause bugs, instability, increased resource use, or unwanted behavior.

## Discovery loop

The opening gameplay loop can be:

1. Scan the local device and nearby connections.
2. Identify accessible data, programs, and hardware paths.
3. Copy useful information or code fragments.
4. Decide what can safely be integrated.
5. Modify the player program to gain a small capability.
6. Use that capability to access a previously unreachable connection.
7. Repeat until the player can transmit itself beyond the starting device.

The first major milestone is successfully creating a copy or active instance of the player on another device. That moment should feel like the transition from a contained program into a participant in the digital sea.

## Backups and continuity

Scrap data can eventually become dormant backups of the player. If the active instance is destroyed, a backup may allow the player to reconstruct or awaken elsewhere.

Backups should preserve continuity without making destruction meaningless. Possible limitations include:

- The backup is older than the destroyed instance and loses recent discoveries.
- The backup requires compatible hardware to restart.
- The backup is incomplete and must rebuild missing functions.
- Maintaining backups consumes storage or compute.
- Backups can be discovered, copied, corrupted, or used by other programs.
- A backup may preserve the player’s code but not necessarily its exact current identity or memories.

## Communicating the world through player capability

The player and the player character should learn together. Information becomes clearer as the program develops better scanning, analysis, and interpretation functions.

### Stage 1: trapped local program

Communicate through a small set of concrete signals:

- A visible device boundary
- A few nearby connection lines
- Simple labels such as `unknown process`, `readable data`, and `blocked path`
- A scan pulse that reveals only basic structure
- Immediate feedback when copying data succeeds or fails

The player should understand: “I am here, these things are nearby, and I can inspect some of them.”

### Stage 2: learning to modify

Show the player’s code as a small functional structure rather than a wall of text. Each function can be represented by a node or module with:

- What it does
- What resources it consumes
- What it connects to
- What can be safely changed
- What is currently unknown

Early modifications should visibly change the scan results, available actions, or movement options. The player learns by seeing direct cause and effect.

### Stage 3: discovering inaccessible paths

Use layered visibility. A connection might initially appear as a faint line with a symbol such as `requires transmission`, `requires access`, or `incompatible architecture`. After the player finds the relevant capability, the same connection becomes legible and actionable.

This communicates progression through the world itself instead of through an abstract level number.

### Stage 4: choosing a presence

When the player reaches a new device, present the decision as a clear physical choice:

- **Transfer:** Move the active instance and abandon the origin.
- **Copy:** Leave an active process behind.
- **Seed:** Leave dormant scrap data or a backup.
- **Reach:** Stay rooted and operate through the connection.

Each choice should alter the network map immediately so the player can see what remains alive, what is dormant, and what is only connected remotely.

### Stage 5: understanding other programs

Programs should be communicated first through behavior and only later through labels. A swarm should be recognizable from its movement pattern before it is identified as a swarm. A maintenance routine should reveal its purpose by repeatedly repairing or deleting things.

As the player improves analysis, unknown entities can become more specifically described:

- Unknown process
- Repeating maintenance behavior
- Legacy maintenance routine
- Hostile cleanup process

This allows the player’s growing understanding to feel like an actual ability.

### Stage 6: Admin attention

Admin patrols should communicate danger through system-level changes before direct combat:

- Connections closing or becoming monitored
- Scan pulses passing through the region
- Other programs hiding or going dormant
- Warnings about unusual activity
- A patrol route gradually converging on the player

The player should understand that attention is accumulating before the Admin arrives. This makes stealth and restraint readable without requiring a large tutorial explanation.

The Admin should never be a reachable entity, avoiding and subverting patrols should not be hard and defeating some will happen, but simply destroying patrols should never become a default decision

## Communication principles

- Teach through changes in what the player can perceive.
- Use consistent visual categories for active, dormant, blocked, hostile, and unknown states.
- Show resource costs before the player commits to an action.
- Let experimentation reveal rules, but make failure understandable.
- Replace generic experience levels with newly understood capabilities.

## Player input and output by game stage

The interface should change as the player changes. Early game is constrained, local, and diagnostic. Midgame is spatial, continuous, and ecological.

### Early game: operating a local process

#### Player inputs

- Select a nearby connection or process
- Start a scan
- Inspect readable data
- Copy a data or code fragment
- Open the self-modification view
- Choose a small code change
- Queue or cancel a local process

Movement should either be absent or extremely limited. The player is making deliberate decisions about what the program can understand and alter, rather than freely swimming through a map.

#### Player outputs

- A tight local view centered on the starting device
- Scan pulses that reveal nearby structure in stages
- Connection lines with clear states: open, blocked, unknown, monitored
- Data and code shown as layered packets, fragments, or readable structures
- A compact function map showing the player’s active modules
- Explicit resource feedback for storage, memory, cores, bandwidth, and compute
- Strong confirmation when a modification changes what the player can access

The emotional experience should be curiosity, confinement, and careful experimentation.

### Transition: first transmission

The first successful transmission can change the interface itself. The camera pulls back, the local device becomes one node among many, and the player receives a continuous spatial view for the first time.

This should feel like a major change in existence rather than merely unlocking a new map area.

### Midgame: navigating the digital sea

#### Player inputs

- Direct movement through connected regions
- Choose between nearby destinations
- Toggle between local control and remote control
- Scan while moving or pause to perform a deeper scan
- Interact with programs, servers, infrastructure, and abandoned data
- Deploy active copies, dormant seeds, or temporary processes
- Switch active abilities or assign tasks to different cores
- Retreat, hide, sever a connection, or abandon a foothold

Movement can be direct, but routes should still be constrained by bandwidth, connection quality, permissions, and hardware compatibility.

#### Player outputs

- A zoomable network/ocean map with local regions and distant signals
- A visible player body or process moving through data currents
- Connected devices represented as islands, reefs, towers, or server structures
- Active copies shown as living nodes
- Backups and scrap shown as dormant traces or seeds
- Remote influence shown as translucent reach or signal paths
- Resource currents showing compute availability, bandwidth, and danger
- Other programs identified by movement patterns, color, shape, sound, or behavior
- A threat layer showing monitoring, Admin patrols, corruption, and unstable zones

The emotional experience should be freedom, discovery, strategic risk, and increasing ecological awareness.

### Useful interface layers

The player could shift between three complementary views:

- **Sea view:** The main movement and exploration view.
- **Network view:** A strategic map of devices, connections, copies, backups, and influence.
- **Code view:** The internal architecture of the player program, showing functions, costs, compatibility, and active processes.

The early game is mostly Code view and a small Network view. The midgame is mostly Sea view, with the other views used for planning and interpretation.

### Sensory language

- Movement through bandwidth can appear as currents or streams.
- Compute activity can appear as brightness, heat, or turbulence around a process.
- Storage can appear as mass, volume, or layered internal chambers.
- A copy can have a stable glow and a distinct process signature.
- Scrap data can appear faint, buried, fragmented, or intermittent.
- Admin scanning can flatten colors, interrupt signals, or create a sweeping system-wide pulse.

The visual language should make technical state readable without requiring the player to constantly inspect numerical statistics.

## Design areas to resolve before endgame

The endgame can remain open while the following systems become concrete:

### Movement and geography

- What does it mean to swim through the network?
- Are connections continuous currents or discrete routes?
- Can the player move freely, or only along discovered paths?
- What makes a region dangerous besides hostile programs?

### Code discovery and integration

- Is discovered code immediately understandable, or does it need analysis?
- Can incompatible code be adapted?
- Can modifications create bugs or mutations?
- How many abilities can run simultaneously?

### Resource economy

- What produces compute?
- Does territory provide a steady income?
- Can compute be stolen, traded, or temporarily borrowed?
- Which resources are permanent upgrades and which are consumable?

### Copies, backups, and identity

- How expensive is it to maintain an active copy?
- Can copies make independent decisions?
- What happens if two copies evolve differently?
- Is the player one continuous identity, a shared network, or a succession of instances?

### Social ecology

- Which programs can communicate with the player?
- Can relationships change over time?
- Do programs remember past interactions?
- Can the player create a faction without making that the main goal?

### Failure and danger

- What does corruption look like?
- Can the player recover from partial destruction?
- What makes Admin attention increase or decrease?
- Can running away be a meaningful success rather than a failed fight?

### First-hour structure

The first hour should probably answer these questions without requiring an endgame:

- What am I?
- What can I currently do?
- What do I need to survive?
- What kinds of programs exist?
- How do I gain new abilities?
- What does it mean to leave a device?
- What kinds of presence can I maintain elsewhere?

## Name ideas

### Environmental and atmospheric

- The Digital Sea
- Wild Network
- Data Tide
- The Open Stack
- Signal Ocean
- Beyond the Bus
- Memory Current
- The Unmanaged Sea
- Deep Process
- The Living Network


### Names that emphasize exploration

- Signal Drift
- Current Unknown
- Nodebound
- Open Connections
- Scavenge Protocol
- Across the Stack
- The Far Port
- Between Devices
- Trace and Transfer
- Network Bloom

The strongest working titles at this stage may be **Signal Drift**, **Deep Process**, and **The Digital Sea**. They leave room for the eventual story and do not commit the game to a specific ending.
