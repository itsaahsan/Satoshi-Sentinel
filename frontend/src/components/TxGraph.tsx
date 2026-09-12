import { useCallback, useEffect, useMemo } from 'react';
import ReactFlow, { Background as FlowBg, Controls, MiniMap, Node, Edge, useNodesState, useEdgesState } from 'reactflow';
import 'reactflow/dist/style.css';
import { api } from '../lib/api';

const RISK_COLOR: Record<string, string> = {
  low: '#22c55e', medium: '#f59e0b', high: '#ef4444',
};

export function TxGraph({ graph, onSelect, wallet }: { graph: { nodes: any[]; edges: any[] }; wallet: string; onSelect: (tx: any) => void }) {
  const initialNodes: Node[] = useMemo(() => (graph.nodes || []).map((n, i) => ({
    id: n.id,
    position: { x: 120 + (i % 3) * 260, y: 60 + Math.floor(i / 3) * 170 },
    data: { label: n.label },
    style: {
      background: '#101625', border: `2px solid ${RISK_COLOR[n.risk] ?? '#22d3ee'}`,
      color: '#e2e8f0', borderRadius: 12, padding: 10, fontSize: 12, width: 180,
    },
  })), [graph]);
  const initialEdges: Edge[] = useMemo(() => (graph.edges || []).map((e) => ({
    id: e.id, source: e.source, target: e.target,
    label: `${e.amount_btc ?? ''} BTC`, animated: true,
    style: { stroke: '#22d3ee' }, labelStyle: { fill: '#94a3b8', fontSize: 10 },
  })), [graph]);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  useEffect(() => { setNodes(initialNodes); setEdges(initialEdges); }, [initialNodes, initialEdges, setNodes, setEdges]);

  const onEdgeClick = useCallback(async (_: any, edge: Edge) => {
    const raw = (graph.edges || []).find((e) => e.id === edge.id);
    if (!raw) return;
    try {
      const r = await api.explain({ txid: raw.txid, direction: raw.source === 'wallet' ? 'sent' : 'received', amount_btc: raw.amount_btc, counterparty: raw.source === 'wallet' ? raw.target : raw.source }, wallet);
      onSelect({ txid: raw.txid, explanation: r.explanation });
    } catch { onSelect({ txid: raw.txid, explanation: 'Could not reach AI service — offline demo mode.' }); }
  }, [graph, wallet, onSelect]);

  return (
    <div className="h-[420px] w-full overflow-hidden rounded-2xl border border-white/10 bg-panel/80">
      <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange}
        onEdgeClick={onEdgeClick} fitView>
        <FlowBg color="#1e293b" gap={28} />
        <Controls /> <MiniMap pannable zoomable />
      </ReactFlow>
    </div>
  );
}
