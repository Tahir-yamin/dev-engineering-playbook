import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter_tts/flutter_tts.dart';

/// Singleton TTS service — speaks card names in Urdu then English.
/// Falls back to Roman Urdu (English engine) when ur-PK voice is not installed.
class TtsService {
  static final TtsService _instance = TtsService._internal();
  factory TtsService() => _instance;

  TtsService._internal() {
    _init().then((_) {
      if (!_initCompleter.isCompleted) _initCompleter.complete();
    }).catchError((e) {
      debugPrint('TtsService init error: $e');
      if (!_initCompleter.isCompleted) _initCompleter.complete();
    });
  }

  final FlutterTts _tts = FlutterTts();
  final Completer<void> _initCompleter = Completer<void>();
  bool _ready = false;
  bool _urduAvailable = false;

  Future<void> _init() async {
    await _tts.setVolume(1.0);
    await _tts.setSpeechRate(0.45);
    await _tts.setPitch(1.1);
    _tts.setErrorHandler((msg) => debugPrint('TtsService error: $msg'));

    // Check Urdu availability once at startup — result is cached
    if (!kIsWeb) {
      _urduAvailable = await _tts.isLanguageAvailable('ur-PK') == true;
      if (!_urduAvailable) {
        debugPrint('TtsService: ur-PK not installed; will use Roman Urdu via en-US');
      }
    }

    _ready = true;
  }

  /// Waits for init to complete (max 5 s) so the first tap is never silent.
  Future<void> _ensureReady() async {
    if (_ready) return;
    await _initCompleter.future.timeout(
      const Duration(seconds: 5),
      onTimeout: () {},
    );
  }

  /// Speaks the card label:
  ///   • If ur-PK voice installed → Urdu script, then English
  ///   • Otherwise               → Roman Urdu (English engine), then English
  Future<void> speakCard(
    String nameUrdu,
    String nameEnglish, {
    String? nameRomanUrdu,
  }) async {
    if (kIsWeb) return;
    await _ensureReady();
    if (!_ready) return;

    try {
      await _tts.stop();

      if (_urduAvailable) {
        await _tts.setLanguage('ur-PK');
        await _tts.speak(nameUrdu);
        await _awaitCompletion();
        await Future.delayed(const Duration(milliseconds: 400));
      } else if (nameRomanUrdu != null && nameRomanUrdu.isNotEmpty) {
        // Roman Urdu is readable by the English engine ("Billi" for بلی)
        await _tts.setLanguage('en-US');
        await _tts.speak(nameRomanUrdu);
        await _awaitCompletion();
        await Future.delayed(const Duration(milliseconds: 300));
      }

      await _tts.setLanguage('en-US');
      await _tts.speak(nameEnglish);
    } catch (e) {
      debugPrint('TtsService.speakCard error: $e');
    }
  }

  /// Speaks a single phrase in the given language, falls back to en-US.
  Future<void> speak(String text, {String language = 'en-US'}) async {
    if (kIsWeb) return;
    await _ensureReady();
    if (!_ready) return;

    try {
      await _tts.stop();

      final langOk = language == 'en-US' ||
          await _tts.isLanguageAvailable(language) == true;
      await _tts.setLanguage(langOk ? language : 'en-US');
      await _tts.speak(text);
    } catch (e) {
      debugPrint('TtsService.speak error: $e');
    }
  }

  Future<void> stop() async {
    try {
      await _tts.stop();
    } catch (_) {}
  }

  /// Resolves when the current utterance completes (or after 4 s safety timeout).
  Future<void> _awaitCompletion() async {
    final c = _SimpleCompleter();
    _tts.setCompletionHandler(c.complete);
    _tts.setErrorHandler((_) => c.complete());
    await c.future.timeout(const Duration(seconds: 4), onTimeout: () {});
    // Restore default error handler
    _tts.setErrorHandler((msg) => debugPrint('TtsService error: $msg'));
  }
}

class _SimpleCompleter {
  final Completer<void> _c = Completer<void>();
  Future<void> get future => _c.future;
  void complete() {
    if (!_c.isCompleted) _c.complete();
  }
}
