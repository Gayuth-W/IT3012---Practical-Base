class KnowledgeBase:
  """A propositional Knowledge Base holding facts and Horn-clause rules.

  facts : set of proposition symbols currently believed true, e.g. "TargetVisible"
  rules : list of ( [premise, ...], conclusion ) tuples, each a Horn clause
          of the form  premise_1 AND premise_2 AND ... => conclusion
  """

  def __init__(self):
    self.facts = set()
    self.rules = []

  def tell_fact(self, fact_string):
    """Assert a single ground fact into the KB."""
    self.facts.add(fact_string)

  def tell_rule(self, premise_list, conclusion_string):
    """Assert a Horn clause: all premises imply the conclusion."""
    self.rules.append((list(premise_list), conclusion_string))

  def clear_facts(self):
    """Drop all facts but keep the rule set (rules are permanent domain knowledge)."""
    self.facts.clear()

  def ask(self, query_string):
    """Return True if the query is currently entailed by the fact base."""
    return query_string in self.facts

  def forward_chain(self):
    """Data-driven forward chaining.

    Repeatedly sweeps the rule list applying Modus Ponens. Each pass that
    adds at least one new fact triggers another pass, so conclusions that
    are themselves premises of later rules get chained. The loop halts when
    a full pass adds nothing, i.e. the fact set has reached a fixed point.
    """
    new_facts_added = True

    while new_facts_added:
      new_facts_added = False

      for premises, conclusion in self.rules:
        if conclusion not in self.facts:
          if all(p in self.facts for p in premises):
            self.facts.add(conclusion)
            new_facts_added = True

    return self.facts