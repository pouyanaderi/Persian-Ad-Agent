from app.copywriting import make_copy

def test_copywriting_has_persian_cta():
    result = make_copy("یک ماگ سرامیکی زیبا", cta="خرید کنید")
    assert "ماگ" in result["caption"]
    assert result["headline"]
    assert "خرید کنید" in result["caption"]

def test_long_headline_is_bounded():
    result = make_copy("محصول", "الف" * 100)
    assert len(result["headline"]) <= 64
