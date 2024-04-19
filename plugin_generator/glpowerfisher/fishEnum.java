package net.runelite.client.plugins.glpowerfisher;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum fishEnum {
    SHRIMP("SHRIMP"),
    SALMON("SALMON"),
    SHARK("SHARK"),
    MONKFISH("MONKFISH"),
    LOBSTER("LOBSTER"),
    TUNA("TUNA"),
    BARBARIAN("BARBARIAN");

    private final String name;

    @Override
    public String toString()
    {
        return getName();
    }
}