import { login } from "@/features/auth/services/authService";
import { AppButton } from "@/shared/components";

export function HomePage() {
 return (
    <div>
        <AppButton variant="contained" onClick={() => login()}>
            Entrar com github
        </AppButton>
    </div>
    );
}