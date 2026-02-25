import React from 'react';

interface MarkdownReportProps {
    content: string;
}

export const MarkdownReport: React.FC<MarkdownReportProps> = ({ content }) => {
    if (!content) return null;

    // Split content into lines
    const lines = content.split('\n');
    const renderedLines: React.ReactNode[] = [];

    let inTable = false;
    let tableHeader: string[] = [];
    let tableRows: string[][] = [];

    const renderTable = (key: string) => {
        if (tableHeader.length === 0) return null;
        return (
            <div key={key} className="my-4 overflow-hidden rounded-lg border border-slate-700 bg-slate-900/50 shadow-sm">
                <table className="w-full text-left text-xs">
                    <thead className="bg-slate-800/80 text-emerald-400">
                        <tr>
                            {tableHeader.map((h, i) => (
                                <th key={i} className="px-4 py-3 font-bold uppercase tracking-wider">{h.trim()}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {tableRows.map((row, i) => (
                            <tr key={i} className="hover:bg-slate-800/30 transition-colors">
                                {row.map((cell, j) => (
                                    <td key={j} className="px-4 py-2.5 text-slate-300 whitespace-nowrap">
                                        {cell.includes('Active') || cell.includes('Normal') || cell.includes('Low') ? (
                                            <span className="text-emerald-400 font-medium">{cell.trim()}</span>
                                        ) : cell.includes('High') || cell.includes('Significant') ? (
                                            <span className="text-red-400 font-medium">{cell.trim()}</span>
                                        ) : (
                                            cell.trim()
                                        )}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        );
    };

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();

        // Table Detection
        if (line.startsWith('|')) {
            if (!inTable) {
                inTable = true;
                // Parse Header
                tableHeader = line.split('|').filter(c => c.trim() !== '').map(c => c.trim());
                tableRows = [];
                continue;
            }

            // Check for separator row (e.g. |---|---|)
            if (line.includes('---')) {
                continue;
            }

            // Parse Row
            const row = line.split('|').filter(c => c.trim() !== '' || line.includes('||')).map(c => c.trim()); // simplified split
            // Better split handling for empty cells if needed, but for now simple filter
            if (row.length > 0) {
                tableRows.push(row);
            }
            continue;
        } else if (inTable) {
            // Table ended
            renderedLines.push(renderTable(`table-${i}`));
            inTable = false;
        }

        // Headers
        if (line.startsWith('### ')) {
            renderedLines.push(<h3 key={i} className="text-emerald-400 font-bold mt-4 mb-2 uppercase tracking-wide text-xs">{line.replace('### ', '')}</h3>);
        } else if (line.startsWith('**') && line.endsWith('**')) {
            renderedLines.push(<h3 key={i} className="text-emerald-400 font-bold mt-4 mb-2 uppercase tracking-wide text-xs">{line.replace(/\*\*/g, '')}</h3>);
        } else if (line.startsWith('# ')) {
            renderedLines.push(<h3 key={i} className="text-emerald-400 font-bold mt-4 mb-2 text-sm">{line.replace('# ', '')}</h3>);
        } else if (line.startsWith('**') && line.includes(':')) {
            // Key-Value style bolding
            const parts = line.split(':');
            renderedLines.push(
                <div key={i} className="mb-1">
                    <span className="text-emerald-400 font-bold">{parts[0].replace(/\*\*/g, '')}:</span>
                    <span className="text-slate-300">{parts.slice(1).join(':')}</span>
                </div>
            );
        }
        // Bullet points
        else if (line.startsWith('- ')) {
            renderedLines.push(<li key={i} className="ml-4 text-slate-300 marker:text-emerald-500">{line.replace('- ', '')}</li>);
        }
        // Standard Text
        else if (line.length > 0) {
            renderedLines.push(<p key={i} className="text-slate-300 mb-1">{line}</p>);
        }
    }

    // Flush remaining table if ends with table
    if (inTable) {
        renderedLines.push(renderTable('table-end'));
    }

    return <div className="font-mono text-[11px] leading-relaxed w-full">{renderedLines}</div>;
};
