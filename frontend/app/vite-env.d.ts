/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_EC_UNIT: string;
    readonly VITE_TEMPERATURE_UNIT: string;
    readonly VITE_HUMIDITY_UNIT: string;
    readonly VITE_NITROGEN_UNIT: string;
    readonly VITE_PHOSPHORUS_UNIT: string;
    readonly VITE_POTASSIUM_UNIT: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}