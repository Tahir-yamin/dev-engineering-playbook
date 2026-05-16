import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:async';
import '../services/antigravity_service.dart';
import '../services/session_tracker.dart';
import '../widgets/symbol_card_widget.dart';
import '../widgets/agent_trace_widget.dart';
import '../data/symbols_data.dart';
import '../models/symbol_card.dart';
import '../services/tts_service.dart';

class GameScreen extends StatefulWidget {
  const GameScreen({super.key});
  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> with TickerProviderStateMixin {
  late AntigravityService _agentService;
  late SessionTracker _tracker;
  final _tts = TtsService();

  String _currentCategory = 'animals';
  List<SymbolCard> _displayCards = [];
  SymbolCard? _targetCard;       // Card the child should find
  bool _showTracePanel = false;  // Toggle for judges
  Timer? _agentCheckTimer;

  // Session score & streak — shown in real-time (Gameplay Engagement criterion)
  int _sessionScore = 0;
  int _currentStreak = 0;
  int _bestStreak = 0;

  // Animation controllers
  late AnimationController _rewardController;
  late AnimationController _cardShakeController;

  @override
  void initState() {
    super.initState();
    _agentService = context.read<AntigravityService>();
    _tracker = context.read<SessionTracker>();

    _rewardController = AnimationController(
      vsync: this, duration: const Duration(milliseconds: 1500));
    _cardShakeController = AnimationController(
      vsync: this, duration: const Duration(milliseconds: 300));

    _loadCards();
    _startAgentCheck();
    // Apply quest category if returning from QuestScreen
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final args = ModalRoute.of(context)?.settings.arguments as Map?;
      final cat = args?['initial_category'] as String?;
      if (cat != null && cat != _currentCategory) {
        _currentCategory = cat;
        _loadCards();
      }
    });
  }

  void _loadCards() {
    if (!mounted) return;
    final allCards = SymbolsData.getCardsByCategory(_currentCategory);
    setState(() {
      _displayCards = (allCards..shuffle()).take(4).toList();
      _targetCard = _displayCards.first;
    });
    _speakTarget();
  }

  /// Announce the target card: "بلی … Billi … Cat"
  Future<void> _speakTarget() async {
    if (_targetCard == null) return;
    await _tts.speakCard(
      _targetCard!.nameUrdu,
      _targetCard!.nameEnglish,
      nameRomanUrdu: _targetCard!.nameRomanUrdu,
    );
  }

  /// Agent evaluation every 30 seconds
  void _startAgentCheck() {
    _agentCheckTimer = Timer.periodic(const Duration(seconds: 30), (_) async {
      final recentEvents = _tracker.getRecentEvents(seconds: 60);
      if (recentEvents.isEmpty) return;

      try {
        final actions = await _agentService.evaluateSession(
          childId: _tracker.childId,
          recentEvents: recentEvents,
        );

        for (final action in actions) {
          _applyAction(action);
        }

        if (mounted) setState(() {});
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Agent check failed — continuing in offline mode'),
              duration: Duration(seconds: 2),
            ),
          );
        }
      }
    });
  }

  void _applyAction(AdaptationAction action) {
    switch (action.type) {
      case 'switch_category':
        // Set category first, then load cards — never call _loadCards inside setState
        _currentCategory = action.data['new_category'] ?? action.data['target'] ?? 'animals';
        _loadCards(); // _loadCards calls setState internally
        break;
      case 'adjust_difficulty':
        final count = (action.data['cards_per_round'] as num?)?.toInt() ?? 4;
        if (count > _displayCards.length) {
          _tracker.recordDifficultyIncrease();
        }
        setState(() {
          _displayCards = (SymbolsData.getCardsByCategory(_currentCategory)..shuffle())
              .take(count.clamp(2, 6)).toList();
          _targetCard = _displayCards.first;
        });
        _speakTarget();
        break;
      case 'trigger_reward':
        _showReward(action.data['praise_phrase'] ?? 'Shabash!');
        break;
      case 'send_break_prompt':
        _showBreakDialog();
        break;
      // A2A delegation: Therapy Director called Story Weaver internally.
      // The quest data is already in action.data — route it to the quest screen.
      case 'generate_quest_via_story_weaver':
        if (action.data.containsKey('quest_title') && mounted) {
          Navigator.pushReplacementNamed(context, '/quest', arguments: action.data);
        }
        break;
    }
  }

  void _onCardTapped(SymbolCard card) {
    final isCorrect = card.id == _targetCard?.id;

    _tracker.recordEvent(
      cardId: card.id,
      category: _currentCategory,
      isSuccess: isCorrect,
    );

    setState(() {
      if (isCorrect) {
        _sessionScore += 10 + _currentStreak * 2; // bonus for streak
        _currentStreak++;
        if (_currentStreak > _bestStreak) _bestStreak = _currentStreak;
      } else {
        _currentStreak = 0;
      }
    });

    if (isCorrect) {
      final praise = _currentStreak >= 3
          ? 'Wah wah! $_currentStreak streak! 🔥'
          : 'Shabash! 🌟';
      _showReward(praise);
      Future.delayed(const Duration(seconds: 2), _loadCards);
    } else {
      _cardShakeController.forward(from: 0);
    }
  }

  void _showReward(String praise) {
    _rewardController.forward(from: 0);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(praise, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF6C63FF),
        duration: const Duration(seconds: 2),
      ),
    );
  }

  void _showBreakDialog() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('🧘 Break Time!'),
        content: const Text('Let\'s take a small break. Stretch, drink water, or give a hug!'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Okay, back to game!'),
          ),
        ],
      ),
    );
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF0EEFF),
      appBar: AppBar(
        backgroundColor: const Color(0xFF6C63FF),
        foregroundColor: Colors.white,
        title: Row(
          children: [
            const Text('⭐ Sitara', style: TextStyle(fontWeight: FontWeight.bold)),
            const Spacer(),
            // BENCHMARK TOGGLE: Switch between agentic AI and fixed-rule heuristic
            GestureDetector(
              onTap: () => setState(() {
                _agentService.useHeuristic = !_agentService.useHeuristic;
              }),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                margin: const EdgeInsets.only(right: 6),
                decoration: BoxDecoration(
                  color: _agentService.useHeuristic
                      ? Colors.grey.withValues(alpha: 0.35)
                      : Colors.white.withValues(alpha: 0.22),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.white.withValues(alpha: 0.45)),
                ),
                child: Text(
                  _agentService.useHeuristic ? '📏 Rules' : '🤖 AI',
                  style: const TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: Colors.white),
                ),
              ),
            ),
            // JUDGE TOGGLE: Show AI reasoning panel
            IconButton(
              icon: Icon(_showTracePanel ? Icons.psychology : Icons.psychology_outlined),
              onPressed: () => setState(() => _showTracePanel = !_showTracePanel),
              tooltip: 'Show AI Reasoning',
            ),
          ],
        ),
      ),
      body: Column(
        children: [
          // Score & streak bar — real-time feedback (Gameplay Engagement)
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                // Category
                Row(children: [
                  const Text('📂 ', style: TextStyle(fontSize: 14)),
                  Text(
                    _currentCategory.toUpperCase(),
                    style: const TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF6C63FF),
                    ),
                  ),
                ]),
                // Score
                Row(children: [
                  const Icon(Icons.star_rounded, color: Color(0xFFFFD700), size: 20),
                  const SizedBox(width: 4),
                  Text(
                    '$_sessionScore',
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w900,
                      color: Color(0xFF333333),
                    ),
                  ),
                ]),
                // Streak
                Row(children: [
                  Text(
                    _currentStreak >= 3 ? '🔥' : '⚡',
                    style: const TextStyle(fontSize: 16),
                  ),
                  const SizedBox(width: 4),
                  Text(
                    '×$_currentStreak',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w900,
                      color: _currentStreak >= 3
                          ? const Color(0xFFFF6B35)
                          : const Color(0xFF6C63FF),
                    ),
                  ),
                ]),
              ],
            ),
          ),

          // ── Target prompt ─────────────────────────────────────────
          if (_targetCard != null)
            GestureDetector(
              // Tap the prompt banner to repeat the voiceover
              onTap: _speakTarget,
              child: Container(
                margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: const [
                    BoxShadow(color: Colors.black12, blurRadius: 10, offset: Offset(0, 3))
                  ],
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Speaker icon — tappable hint
                    const Icon(Icons.volume_up_rounded, color: Color(0xFF6C63FF), size: 24),
                    const SizedBox(width: 10),

                    // Urdu name (RTL)
                    Text(
                      _targetCard!.nameUrdu,
                      textDirection: TextDirection.rtl,
                      style: const TextStyle(
                        fontSize: 26,
                        fontWeight: FontWeight.w900,
                        color: Color(0xFF6C63FF),
                        height: 1.1,
                      ),
                    ),

                    // Divider dot
                    const Padding(
                      padding: EdgeInsets.symmetric(horizontal: 8),
                      child: Text('·', style: TextStyle(fontSize: 22, color: Colors.grey)),
                    ),

                    // English name
                    Text(
                      _targetCard!.nameEnglish,
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.w600,
                        color: Color(0xFF555555),
                      ),
                    ),
                  ],
                ),
              ),
            ),

          // Symbol card grid
          Expanded(
            child: GridView.builder(
              padding: const EdgeInsets.all(16),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                childAspectRatio: 1.0,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
              ),
              itemCount: _displayCards.length,
              itemBuilder: (ctx, i) {
                final card = _displayCards[i];
                final isTarget = card.id == _targetCard?.id;
                return SymbolCardWidget(
                  card: card,
                  // Correct card: suppress widget TTS — _loadCards → _speakTarget handles it.
                  // Wrong card:   speak so the child hears what they tapped (AAC feedback).
                  speakOnTap: !isTarget,
                  onTap: () => _onCardTapped(card),
                );
              },
            ),
          ),

          // Antigravity trace panel (for judges)
          if (_showTracePanel)
            AgentTraceWidget(traces: _agentService.traceLog),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _agentCheckTimer?.cancel();
    _rewardController.dispose();
    _cardShakeController.dispose();
    _tts.stop(); // Stop any in-progress utterance when leaving screen
    super.dispose();
  }
}
