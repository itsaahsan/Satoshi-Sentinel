export type Lesson = { id: string; title: string; level: 'Beginner' | 'Intermediate' | 'Advanced'; body: string; icon: string };

export const LESSONS: Lesson[] = [
  { id: 'addr', title: 'Bitcoin addresses', level: 'Beginner', icon: '🔑', body: 'Addresses are like invoice numbers derived from public keys. Sharing one lets anyone view its full history — so treat every address as public once shared.' },
  { id: 'reuse', title: 'Address reuse', level: 'Beginner', icon: '♻️', body: 'Receiving twice to one address links both payments trivially. Modern wallets generate fresh addresses automatically — let them.' },
  { id: 'utxo', title: 'UTXOs & coin control', level: 'Intermediate', icon: '🪙', body: 'Your balance is a set of unspent outputs (UTXOs). Spending merges inputs and publicly declares common ownership. Coin control = choosing which coins to spend.' },
  { id: 'txpriv', title: 'Transaction privacy', level: 'Intermediate', icon: '🕵️', body: 'Amounts, timing, counterparties and change outputs are all metadata. Observers cluster wallets with heuristics like common-input ownership.' },
  { id: 'cj', title: 'CoinJoin', level: 'Advanced', icon: '🌀', body: 'Collaborative transactions blur sender/receiver links. Understand coordinators, fees, liquidity and post-mix hygiene before use.' },
  { id: 'ln', title: 'Lightning privacy', level: 'Intermediate', icon: '⚡', body: 'Lightning keeps small payments off-chain — only opens/closes hit the ledger. Routing nodes still see forwarding amounts.' },
  { id: 'nostr', title: 'Nostr identity', level: 'Beginner', icon: '💜', body: 'Nostr identities are keypairs (npub/nsec), no accounts or servers. Share tips freely — never publish seeds, keys, or balances.' },
  { id: 'custody', title: 'Self-custody basics', level: 'Beginner', icon: '🔒', body: 'Hold your own keys with a hardware wallet + offline seed backup. Verify receive addresses on-device; start with small test sends.' },
  { id: 'transparency', title: 'Public ledger transparency', level: 'Beginner', icon: '🔍', body: 'Anyone can audit any address on mempool.space or block explorers. Privacy = limiting what gets linked to you, not hiding the ledger.' },
];

export const CHECKLIST = [
  'Use a fresh address for every receive',
  'Keep public (donation) and private funds in separate wallets',
  'Learn coin control before consolidating UTXOs',
  'Never post addresses alongside your real identity',
  'Verify receive addresses on your hardware device',
  'Never share seed phrases or private keys with anyone',
];
