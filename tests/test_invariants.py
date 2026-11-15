"""Properties every hit and every call must keep, whatever the patterns say."""
import pytest

from institutional_markers import MARKER_VERSIONS, MARKERS, PACKAGE_VERSION, scan
from institutional_markers._fold import fold

SAMPLES = [
    ("en", "Two protesters were killed on Tuesday, the ministry claimed that police acted lawfully."),
    ("en", '"Mistakes were made," the minister said. The waiver is granted.'),
    ("en", "ÉMIGRÉ İstanbul straße — “quoted” ‘single’ text; the account was suspended."),
    ("pt", "Fica dispensada a licitação, em caráter emergencial. Cabe à ré comprovar o pagamento."),
    ("pt", "Foram mortos dois manifestantes. O deputado teria desviado verbas, segundo relatos."),
    ("pt", "«Reconhecemos o erro», admitiu o diretor. A decisão é irrecorrível."),
]


@pytest.mark.parametrize("text", [t for _, t in SAMPLES] + ["", "ß İ ﬁ ǅ Å", "áb"])
def test_fold_keeps_length(text):
    assert len(fold(text)) == len(text)


@pytest.mark.parametrize("lang,text", SAMPLES)
def test_every_hit_is_a_verbatim_span(lang, text):
    for h in scan(text, lang=lang, include_defined=True):
        assert h.quote == text[h.start:h.end]
        assert 0 <= h.start < h.end <= len(text)
        assert h.version == MARKER_VERSIONS[h.marker]
        assert h.subtype is None or h.subtype in MARKERS[h.marker].subtypes
        assert h.pattern_id.startswith(lang + ":")


@pytest.mark.parametrize("lang,text", SAMPLES)
def test_default_returns_only_invoked(lang, text):
    assert all(h.invoked for h in scan(text, lang=lang))
    defined = scan(text, lang=lang, include_defined=True)
    assert {h for h in defined if h.invoked} == set(scan(text, lang=lang))


@pytest.mark.parametrize("lang,text", SAMPLES)
def test_hits_are_sorted_and_one_per_region_per_marker(lang, text):
    hits = scan(text, lang=lang, include_defined=True)
    assert hits == sorted(hits, key=lambda h: (h.start, h.end, h.marker))
    for a in hits:
        for b in hits:
            if a is not b and a.marker == b.marker:
                assert a.end <= b.start or b.end <= a.start


def test_scan_is_deterministic():
    lang, text = SAMPLES[0]
    assert scan(text, lang=lang) == scan(text, lang=lang)


def test_exclude_makes_hits_not_invoked():
    text = "The waiver is granted."
    assert scan(text)[0].invoked
    hits = scan(text, exclude=[(0, len(text))], include_defined=True)
    assert hits and not any(h.invoked for h in hits)
    assert scan(text, exclude=[(0, len(text))]) == []


def test_markers_filter():
    text = "Two protesters were killed, the ministry claimed that it was lawful."
    assert {h.marker for h in scan(text, markers=["hedge", "attribution_verb"])} == {"attribution_verb"}


def test_rejects_unknown_lang_and_marker():
    with pytest.raises(ValueError):
        scan("x", lang="de")
    with pytest.raises(ValueError):
        scan("x", markers=["framing"])


def test_registry_shape():
    assert set(MARKERS) == {"exception_clause", "burden", "discretion",
                            "agentless_passive", "hedge", "attribution_verb"}
    assert {m.group for m in MARKERS.values()} == {"institutional", "comparison"}
    assert PACKAGE_VERSION.count(".") == 2
