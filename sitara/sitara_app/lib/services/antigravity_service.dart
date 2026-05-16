import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/session_event.dart';

class AntigravityService extends ChangeNotifier {
  // Override at build time: flutter run --dart-define=BACKEND_URL=http://10.0.2.2:8000
  static const String _baseUrl = String.fromEnvironment(
    'BACKEND_URL',
    defaultValue: 'https://sitara-backend-178558547254.asia-south1.run.app',
  );

  // Trace log for judge panel — stored locally, shown in UI
  final List<TraceEntry> traceLog = [];

  /// Toggle for "Sovereign Benchmarking": Baseline (Heuristic) vs Agentic
  bool _useHeuristic = false;
  bool get useHeuristic => _useHeuristic;
  set useHeuristic(bool val) {
    _useHeuristic = val;
    notifyListeners();
  }

  // ─── BASELINE COMPARISON ACCUMULATORS ───────────────────────────────
  int agentSessions = 0;
  int baselineSessions = 0;
  double _agentSuccessSum = 0;
  double _baselineSuccessSum = 0;

  double get agentAvgSuccess =>
      agentSessions == 0 ? 0 : _agentSuccessSum / agentSessions;
  double get baselineAvgSuccess =>
      baselineSessions == 0 ? 0 : _baselineSuccessSum / baselineSessions;

  /// Client-side heuristic — mirrors backend get_heuristic_adaptation().
  /// Runs entirely in Flutter; no API call needed in baseline mode.
  List<AdaptationAction> _heuristicAdaptation(Map<String, dynamic> summary) {
    final consecutiveFails =
        (summary['consecutive_failures'] as num?)?.toInt() ?? 0;
    final successRate = (summary['success_rate'] as num?)?.toDouble() ?? 0.0;
    final sessionMins =
        (summary['session_duration_mins'] as num?)?.toDouble() ?? 0.0;
    final cardsAttempted =
        (summary['total_attempts'] as num?)?.toInt() ?? 0;

    if (consecutiveFails >= 3 || successRate < 0.3) {
      return [
        AdaptationAction(type: 'adjust_difficulty', data: {
          'cards_per_round': 2,
          'card_size': 'large',
          'reason': 'Heuristic: high frustration',
        })
      ];
    }
    if (successRate > 0.7 && cardsAttempted > 0 && cardsAttempted % 5 == 0) {
      return [
        AdaptationAction(type: 'trigger_reward', data: {
          'reward_type': 'star',
          'praise_phrase': 'Shabash! Bohat acha!',
          'milestone_achieved': 'consistent_success',
        })
      ];
    }
    if (sessionMins > 10 && successRate < 0.5) {
      return [
        AdaptationAction(type: 'send_break_prompt', data: {'break_type': 'stretch'})
      ];
    }
    return [];
  }

  // ─── THERAPY DIRECTOR ───────────────────────────────────────────────

  /// Called every 30 seconds during active session
  Future<List<AdaptationAction>> evaluateSession({
    required String childId,
    required List<SessionEvent> recentEvents,
  }) async {
    final sessionSummary = _summariseEvents(recentEvents);
    final double successRate =
        (sessionSummary['success_rate'] as num?)?.toDouble() ?? 0.0;

    // ── BASELINE MODE: run client-side heuristic, skip API ──────────
    if (_useHeuristic) {
      final actions = _heuristicAdaptation(sessionSummary);
      _addTrace(
        agent: 'Heuristic Baseline',
        reasoning:
            'Fixed-rule adaptation (no agent inference). '
            'consecutive_failures=${sessionSummary['consecutive_failures']}, '
            'success_rate=${successRate.toStringAsFixed(2)}',
        actions: actions,
      );
      baselineSessions++;
      _baselineSuccessSum += successRate;
      notifyListeners();
      return actions;
    }

    // ── AGENTIC MODE: call Therapy Director ─────────────────────────
    final response = await _post(
      endpoint: 'evaluate-session',
      body: {
        'child_id': childId,
        'success_rate': sessionSummary['success_rate'] ?? 0.0,
        'consecutive_failures': sessionSummary['consecutive_failures'] ?? 0,
        'tap_speed': sessionSummary['avg_tap_speed'] ?? 0.0,
        'category': sessionSummary['current_category'] ?? 'animals',
        'session_duration_mins': sessionSummary['session_duration_mins'] ?? 0.0,
        'cards_attempted': sessionSummary['total_attempts'] ?? 0,
      },
    );

    // Parse agent actions from response
    final actions = _parseActions(response['actions']);

    final mode = response['mode'] as String? ?? 'agentic';

    // Log trace for judge panel
    _addTrace(
      agent: mode == 'agentic' ? 'Therapy Director' : 'Sovereign Baseline',
      reasoning: response['reasoning'] ?? '',
      actions: actions,
    );

    // Track metrics based on response mode
    if (mode == 'agentic') {
      agentSessions++;
      _agentSuccessSum += successRate;
    } else {
      // Includes 'baseline' and 'baseline_fallback'
      baselineSessions++;
      _baselineSuccessSum += successRate;
    }
    
    notifyListeners();

    return actions;
  }

  // ─── STORY WEAVER ───────────────────────────────────────────────────

  /// Request a personalised quest — returns raw Map so QuestScreen can consume directly.
  Future<Map<String, dynamic>> generateQuest({
    required String childId,
    required String preferredCategory,
    required String childName,
    required String difficulty,
  }) async {
    final response = await _post(
      endpoint: 'generate-quest',
      body: {
        'child_id': childId,
        'child_name': childName,
        'preferred_category': preferredCategory,
        'difficulty': difficulty,
      },
    );

    // /generate-quest returns quest fields at top-level (see _post wrapper)
    final questMap = response['quest'] as Map<String, dynamic>? ?? response;

    final mode = response['mode'] as String? ?? 'agentic';
    final qcStatus = questMap['qc_status'] as String? ?? '?';
    _addTrace(
      agent: mode == 'agentic' ? 'Story Weaver [QC: $qcStatus]' : 'Sovereign Baseline',
      reasoning: 'Generated personalised quest for $childName',
      actions: [AdaptationAction(type: 'quest_generated', data: questMap)],
    );

    return questMap;
  }

  // ─── PROGRESS GUARDIAN ──────────────────────────────────────────────

  /// Generate weekly parent report
  Future<String> generateWeeklyReport(
    String childId, {
    String childName = 'Your Child',
    Map<String, dynamic>? weekSummary,
  }) async {
    final summary = weekSummary ?? _buildWeekSummary();

    final response = await _post(
      endpoint: 'weekly-report',
      body: {
        'child_id': childId,
        'child_name': childName,
        'session_summary': jsonEncode(summary),
        'therapist_insights': _extractInsightsFromTrace(),
      },
    );

    final mode = response['mode'] as String? ?? 'agentic';
    _addTrace(
      agent: mode == 'agentic' ? 'Progress Guardian' : 'Sovereign Baseline',
      reasoning: 'Generated weekly parent report for $childName',
      actions: [],
    );

    return response['report'] as String? ?? 'Report generated.';
  }

  /// Build a basic session summary from in-memory trace log
  Map<String, dynamic> _buildWeekSummary() {
    final total = traceLog.length;
    final adaptations = traceLog.expand((t) => t.actions).toList();
    return {
      'sessions_logged': total,
      'total_adaptations': adaptations.length,
      'categories_explored': adaptations.where((a) => a.contains('category')).length,
      'rewards_triggered': adaptations.where((a) => a.contains('reward')).length,
    };
  }

  /// Extract insight descriptions from trace log for Progress Guardian
  String _extractInsightsFromTrace() {
    final insights = traceLog
        .where((t) => t.agent == 'Therapy Director' && t.reasoning.isNotEmpty)
        .map((t) => t.reasoning)
        .take(5)
        .join(' | ');
    return insights.isEmpty ? 'No insights recorded yet.' : insights;
  }

  // ─── INTERNAL ───────────────────────────────────────────────────────

  Future<Map<String, dynamic>> _post({
    required String endpoint,
    required Map<String, dynamic> body,
  }) async {
    try {
      final res = await http
          .post(
            Uri.parse('$_baseUrl/$endpoint'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(body),
          )
          .timeout(const Duration(seconds: 10));

      if (res.statusCode == 200) {
        final data = jsonDecode(res.body) as Map<String, dynamic>;
        if (endpoint == 'generate-quest') {
          return {'quest': data};
        }
        return data;
      } else {
        return _localFallback(endpoint);
      }
    } catch (e) {
      return _localFallback(endpoint);
    }
  }

  /// LOCAL FALLBACK: Rule-based adaptation when offline
  /// This ensures the app works without internet (critical for Pakistan)
  Map<String, dynamic> _localFallback(String endpoint) {
    if (endpoint == 'evaluate-session') {
      return {
        'mode': 'offline',
        'reasoning': '[𝐎𝐅𝐅𝐋𝐈𝐍𝐄 𝐌𝐎𝐃𝐄] Using local rules: high consecutive failures → switch category',
        'actions': [
          {'tool': 'switch_category', 'args': {'target_category': 'animals', 'reason': 'Offline fallback'}}
        ]
      };
    }
    return {'reasoning': 'Offline mode', 'actions': []};
  }

  Map<String, dynamic> _summariseEvents(List<SessionEvent> events) {
    if (events.isEmpty) return {};
    final successes = events.where((e) => e.isSuccess).length;
    final avgTapSpeed =
        events.map((e) => e.tapSpeed).reduce((a, b) => a + b) / events.length;
    final consecutiveFails = _countConsecutiveFails(events);

    return {
      'total_attempts': events.length,
      'successes': successes,
      'failures': events.length - successes,
      'success_rate': successes / events.length,
      'avg_tap_speed': avgTapSpeed,
      'consecutive_failures': consecutiveFails,
      'current_category': events.last.category,
      'session_duration_mins': 0.0,
    };
  }

  int _countConsecutiveFails(List<SessionEvent> events) {
    int count = 0;
    for (final e in events.reversed) {
      if (!e.isSuccess) {
        count++;
      } else {
        break;
      }
    }
    return count;
  }

  List<AdaptationAction> _parseActions(dynamic actionsJson) {
    if (actionsJson is! List) return [];
    return actionsJson
        .whereType<Map<String, dynamic>>()
        .map((a) => AdaptationAction.fromJson(a))
        .toList();
  }

  void _addTrace({
    required String agent,
    required String reasoning,
    required List<AdaptationAction> actions,
  }) {
    traceLog.add(TraceEntry(
      timestamp: DateTime.now(),
      agent: agent,
      reasoning: reasoning,
      actions: actions.map((a) => a.type).toList(),
    ));
  }

  /// Export traces for hackathon submission
  String exportTracesAsJson() =>
      jsonEncode(traceLog.map((t) => t.toJson()).toList());
}

class AdaptationAction {
  final String type;
  final Map<String, dynamic> data;

  AdaptationAction({required this.type, Map<String, dynamic>? data})
      : data = data ?? {};

  factory AdaptationAction.fromJson(Map<String, dynamic> json) =>
      AdaptationAction(
        type: json['tool'] as String? ?? 'unknown',
        data: (json['args'] as Map<String, dynamic>?) ?? {},
      );
}

class TraceEntry {
  final DateTime timestamp;
  final String agent;
  final String reasoning;
  final List<String> actions;

  TraceEntry({
    required this.timestamp,
    required this.agent,
    required this.reasoning,
    required this.actions,
  });

  Map<String, dynamic> toJson() => {
        'timestamp': timestamp.toIso8601String(),
        'agent': agent,
        'reasoning': reasoning,
        'actions': actions,
      };
}

class Quest {
  final String title;
  final String storyText;
  final String targetCategory;
  final String urduHook;

  Quest({
    required this.title,
    required this.storyText,
    required this.targetCategory,
    required this.urduHook,
  });

  factory Quest.fromJson(Map<String, dynamic> json) => Quest(
        title: json['quest_title'] as String? ?? 'New Adventure!',
        storyText: json['story_text'] as String? ?? '',
        targetCategory: json['target_category'] as String? ?? 'animals',
        urduHook: json['urdu_hook'] as String? ?? 'Chalo!',
      );
}
