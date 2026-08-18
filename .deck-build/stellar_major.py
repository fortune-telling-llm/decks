from stellar_base import *

MAJORS = [
(57,'The Fool','beginnings, trust, and freedom at the edge of the unknown','a radiant traveler steps toward a cliff with a white rose and small dog while a spiral galaxy opens beyond the mountains'),
(58,'The Magician','focused agency and the ability to translate potential into deliberate action','a standing figure raises a wand above a table holding cup, sword, pentacle, and wand beneath an infinity halo'),
(59,'The High Priestess','inner knowing, mystery, and knowledge protected until the right moment','a veiled priestess sits between black and white pillars before a pomegranate curtain, moon at her feet and scroll in hand'),
(60,'The Empress','fertility, creation, pleasure, and life supported through embodied care','a crowned figure rests among wheat, river, forest, roses, and a heart-shaped Venus shield beneath twelve stars'),
(61,'The Emperor','structure, protection, authority, and the responsibility carried by power','an armored ruler sits on a ram-carved stone throne above a dry mountain kingdom with a red mantle and square halo'),
(62,'The Hierophant','tradition, teaching, initiation, and the question of which systems deserve trust','a spiritual teacher raises two fingers between pillars while two students kneel before crossed keys and layered sacred geometry'),
(63,'The Lovers','value-aligned choice, intimacy, and relationship that reveals the self','two figures stand beneath an angel between a fruit tree, a flame tree, a mountain, and a descending sun'),
(64,'The Chariot','directed will, integration of opposing drives, and movement earned through self-command','a crowned charioteer stands in a star canopy above black and white sphinxes with no visible reins'),
(65,'Strength','courage through compassionate regulation rather than domination','a calm figure gently closes a lion’s jaws beneath an infinity halo while roses and a distant mountain frame the meeting'),
(66,'The Hermit','solitude, discernment, and guidance found by carrying one honest light','a cloaked elder stands on a snowy summit holding a six-pointed lantern and staff beneath a sparse night sky'),
(67,'Wheel of Fortune','cycles, turning conditions, and the meeting of fate with response','a great wheel bearing letters and alchemical signs turns among clouds, guarded by a sphinx, serpent, and winged readers'),
(68,'Justice','truth, consequence, and balance created through accountable decisions','a seated figure holds upright sword and level scales between pillars, framed by a square veil and clear red light'),
(69,'The Hanged Man','suspension, surrender, and insight gained through a changed perspective','a serene figure hangs by one foot from a living tree, forming a reversed triangle with a bright halo around the head'),
(70,'Death','irreversible transition, release, and the clearing required for renewal','a skeletal rider carries a black banner past fallen rank, grieving figures, a child, and a sunrise between towers'),
(71,'Temperance','integration, healing, and the patient creation of a third way','an angel pours water between two cups with one foot on land and one in water, a path rising toward a radiant crown'),
(72,'The Devil','attachment, compulsion, and power surrendered through unexamined bargains','a horned figure presides above two loosely chained people whose restraints can be removed, with an inverted torch below'),
(73,'The Tower','sudden revelation, collapse of false structure, and liberation through undeniable truth','lightning strikes a crowned tower as fire bursts from windows and two figures fall into a black-gold storm'),
(74,'The Star','renewal, honesty, and hope grounded in unguarded participation','a kneeling figure pours water onto pool and earth beneath one great star and seven smaller stars, watched by a bird'),
(75,'The Moon','uncertainty, instinct, projection, and navigation without full visibility','a moon with three phases hangs between towers while dog and wolf call across a path where a crayfish leaves the water'),
(76,'The Sun','clarity, vitality, and joy made safe enough to be openly shared','a child rides a white horse beneath a vast sun, carrying a red banner before sunflowers and a low garden wall'),
(77,'Judgement','awakening, reckoning, and answering a call that changes identity','an angel sounds a trumpet over rising figures whose open arms form a collective response beneath distant mountains'),
(78,'The World','completion, integration, and belonging within a larger living whole','a dancing figure moves inside a laurel oval while human, eagle, lion, and bull occupy the four corners of the cosmos'),
]

CHALLENGING = {'Five of Cups','Five of Pentacles','Three of Swords','Five of Swords','Eight of Swords','Nine of Swords','Ten of Swords','The Devil','The Tower','The Moon'}
SLOW = {'Seven of Pentacles','Knight of Pentacles','The Hanged Man','Temperance','The Hermit'}
