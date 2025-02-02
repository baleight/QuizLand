from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    """Template filter per ottenere un valore da un dizionario"""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def get_question_options(question):
    """Template filter per ottenere le opzioni della domanda"""
    return [
        ('A', question.option_a),
        ('B', question.option_b),
        ('C', question.option_c),
        ('D', question.option_d)
    ]

@register.filter
def get_option_text(options_list, letter):
    """Template filter per ottenere il testo di un'opzione specifica"""
    for opt_letter, opt_text in options_list:
        if opt_letter == letter:
            return opt_text
    return ''

@register.filter
def get_duration(assignment):
    """
    Calcola la durata di un quiz.
    """
    if assignment.completed_at and assignment.assigned_date:
        duration = assignment.completed_at - assignment.assigned_date
        minutes = duration.seconds // 60
        return f"{minutes} minuti"
    return "N/A" 